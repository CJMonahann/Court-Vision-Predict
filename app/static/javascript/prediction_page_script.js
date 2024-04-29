// Wait for the DOM content to be loaded before adding event listener
document.addEventListener("DOMContentLoaded", function() {
    // Function to load user predictions from the server
    function loadUserPredictions() {
        // Iterate through each prediction form
        predictionForms.forEach(function(predictionForm) {
            // Load previously submitted prediction from database, if any
            var userPrediction = predictionForm.nextElementSibling;
            var formId = predictionForm.dataset.formId;

            // Make AJAX request to fetch prediction for the current form
            fetch('/prediction/submit?user_id=1&form_id=' + formId)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Display the user's prediction
                    userPrediction.style.display = "block";
                    var predictionDisplay = userPrediction.querySelector(".userPredictionDisplayText");
                    predictionDisplay.textContent = data.prediction;
                    predictionForm.style.display = "none";
                }
            })
            .catch(error => {
                // Handle error
                console.error('Error:', error);
            });
        });
    }
    // Select all prediction forms
    var predictionForms = document.querySelectorAll(".predictionForm");

    // Call the function to load user predictions when the page loads
    loadUserPredictions();
        
    // Loop through each prediction form
    predictionForms.forEach(function(predictionForm) {
        // Select the submit button within the current form
        var submitButton = predictionForm.querySelector('input[type="submit"]');

        // Initially disable the submit button
        submitButton.disabled = true;

        // Select all radio buttons within the current form
        var radioButtons = predictionForm.querySelectorAll('input[type="radio"]');

        // Add change event listener to each radio button
        radioButtons.forEach(function(radioButton) {
            radioButton.addEventListener("change", function() {
                // Check if any radio button is selected
                var anySelected = Array.from(radioButtons).some(function(button) {
                    return button.checked;
                });
                // Enable or disable the submit button based on selection
                submitButton.disabled = !anySelected;
            });
        });

        // Add submit event listener to the current form
        predictionForm.addEventListener("submit", function(event) {
            // Prevent the default form submission behavior
            event.preventDefault();

            // Serialize form data
            var formData = new FormData(predictionForm);

            // Send form data via AJAX
            fetch('/prediction/submit', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Hide the prediction form
                    predictionForm.style.display = "none";

                    // Show the user's prediction
                    var userPrediction = predictionForm.nextElementSibling;
                    userPrediction.style.display = "block";

                    // Retrieve the selected prediction
                    var selectedTeam = predictionForm.querySelector('input[name="prediction"]:checked');
            
                    // If a prediction was selected, display it
                    if (selectedTeam) {
                        var prediction = selectedTeam.value;
                        var predictionDisplay = userPrediction.querySelector(".userPredictionDisplayText");
                        predictionDisplay.textContent = prediction;
                        
                    }
                } else {
                    // Handle error
                    console.error(data.message);
                }
            })
            .catch(error => {
                // Handle network error
                console.error('Error:', error);
            });
        });
    });
});

// Wait for the DOM content to be loaded before adding event listener
document.addEventListener("DOMContentLoaded", function() {
    // Select all prediction forms
    var predictionForms = document.querySelectorAll(".predictionForm");

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
        });
    });
});

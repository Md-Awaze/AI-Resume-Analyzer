// Constants
const NOTIFICATION_DURATION = 5000; // 5 seconds
const ANIMATION_DURATION = 300; // 300ms

// DOM Elements
const notificationBanner = document.getElementById('notification-banner');
const analysisContainer = document.getElementById('analysis-container');
const skillsSection = document.querySelector('.skills-list');
const suggestionsSection = document.querySelector('.suggestions-list');
const scoreValue = document.querySelector('.score-value');
const scoreCircle = document.querySelector('.score-circle');

/**
 * Display analysis results in the UI
 * @param {Object} jsonData - The analysis results data
 */
function displayAnalysisResults(jsonData) {
    try {
        // Update skills section
        updateSkillsSection(jsonData.skills);
        
        // Update suggestions section
        updateSuggestionsSection(jsonData.suggestions);
        
        // Update match score
        animateScoreDisplay(jsonData.matchScore);
        
        // Update status
        updateNotificationStatus(jsonData.status, 'success');
        
    } catch (error) {
        handleError('Failed to display analysis results: ' + error.message);
    }
}

/**
 * Update the skills section with detected skills
 * @param {string[]} skills - Array of detected skills
 */
function updateSkillsSection(skills) {
    skillsSection.innerHTML = '';
    skills.forEach(skill => {
        const skillElement = document.createElement('span');
        skillElement.className = 'skill-tag';
        skillElement.textContent = skill;
        skillsSection.appendChild(skillElement);
    });
}

/**
 * Update the suggestions section with improvement suggestions
 * @param {string[]} suggestions - Array of improvement suggestions
 */
function updateSuggestionsSection(suggestions) {
    suggestionsSection.innerHTML = '';
    suggestions.forEach(suggestion => {
        const suggestionElement = document.createElement('li');
        suggestionElement.className = 'suggestion-item';
        suggestionElement.textContent = suggestion;
        suggestionsSection.appendChild(suggestionElement);
    });
}

/**
 * Animate the score display with a circular progress indicator
 * @param {number} score - The match score (0-100)
 */
function animateScoreDisplay(score) {
    // Ensure score is between 0 and 100
    score = Math.min(Math.max(score, 0), 100);
    
    // Update the score value
    scoreValue.textContent = Math.round(score);
    
    // Update the circular progress
    scoreCircle.style.background = `conic-gradient(var(--primary-color) ${score * 3.6}deg, #eee ${score * 3.6}deg)`;
    
    // Add animation class
    scoreCircle.classList.add('animate');
    
    // Remove animation class after animation completes
    setTimeout(() => {
        scoreCircle.classList.remove('animate');
    }, ANIMATION_DURATION);
}

/**
 * Update the notification banner with a message
 * @param {string} message - The message to display
 * @param {string} type - The type of notification (success, error, warning)
 */
function updateNotificationStatus(message, type) {
    // Clear any existing timeout
    if (notificationBanner.timeout) {
        clearTimeout(notificationBanner.timeout);
    }
    
    // Update notification content and type
    notificationBanner.textContent = message;
    notificationBanner.className = `notification-banner ${type}`;
    
    // Show the notification
    notificationBanner.classList.add('show');
    
    // Hide the notification after duration
    notificationBanner.timeout = setTimeout(() => {
        notificationBanner.classList.remove('show');
    }, NOTIFICATION_DURATION);
}

/**
 * Handle errors and display them in the notification banner
 * @param {string} errorMessage - The error message to display
 */
function handleError(errorMessage) {
    console.error(errorMessage);
    updateNotificationStatus(errorMessage, 'error');
}

// Example usage with sample data
const sampleData = {
    skills: ['JavaScript', 'Python', 'React', 'Node.js', 'SQL'],
    suggestions: [
        'Add more details about your project achievements',
        'Include relevant certifications',
        'Highlight leadership experience'
    ],
    matchScore: 85,
    status: 'Analysis completed successfully'
};

// Initialize the display with sample data
document.addEventListener('DOMContentLoaded', () => {
    displayAnalysisResults(sampleData);
}); 
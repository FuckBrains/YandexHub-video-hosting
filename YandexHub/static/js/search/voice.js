//Voice Search
/* setup vars for our trigger, form, text input and result elements */
var $voiceTrigger = $("#voice-trigger");
var $searchInput = $("#search-input");
var $result = $("#result");


/*  set Web Speech API for Chrome or Firefox */
window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

/* Check if browser support Web Speech API, remove the voice trigger if not supported */
if (window.SpeechRecognition) {

    /* setup Speech Recognition */
    var recognition = new SpeechRecognition();
    recognition.interimResults = true;
    recognition.lang = 'ru-RU';
    recognition.lang = 'en-EN';
    recognition.addEventListener('result', _transcriptHandler);

    recognition.onerror = function (event) {
        console.log(event.error);
    }
} else {
    $voiceTrigger.remove();
}

jQuery(document).ready(function () {

    /* Trigger listen event when our trigger is clicked */
    $voiceTrigger.on('click touch', listenStart);
});

/* Our listen event */
function listenStart(e) {
    e.preventDefault();
    /* Update input and icon CSS to show that the browser is listening */
    $searchInput.attr("placeholder", "Speak...");
    $voiceTrigger.addClass('voice-trigger-active');
    /* Start voice recognition */
    recognition.start();
}

/* Parse voice input */
function _parseTranscript(e) {
    return Array.from(e.results).map(function (result) { return result[0] }).map(function (result) { return result.transcript }).join('')
}

/* Convert our voice input into text and submit the form */
function _transcriptHandler(e) {
    var speechOutput = _parseTranscript(e)
    document.getElementById("search-input").value = speechOutput;
    if (e.results[0].isFinal) {
        return
    }
}
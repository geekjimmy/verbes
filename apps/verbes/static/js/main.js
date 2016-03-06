$(document).ready(function () {
  // Allow first page to be deleted when Dom caching is disabled:
  // https://github.com/jquery/jquery-mobile/issues/3249
  $('#attempt-page').on('pagehide',function(event){
    $('#attempt-page').remove();
  });

  $('#results-page').on('pagehide',function(event){
    $('#results-page').remove();
  });
});

$(document).delegate("#attempt-page", "pageshow", function () {
  $("#id_answer").focus();

  var onAnswerInput = function () {
    if ($(this).val().length === 0) {
      $("#submit-attempt").addClass('ui-state-disabled');
    } else {
      $("#submit-attempt").removeClass('ui-state-disabled');
    }
  };
  $("#id_answer").on("input", onAnswerInput);

});

$(document).delegate("#attempt-feedback-page", "pageshow", function() {
  $("#continue.focus").focus();
});

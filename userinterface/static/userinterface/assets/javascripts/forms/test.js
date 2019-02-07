
var count=0;

function add() {
  if(count<2)
  {
    count++;
    var objTo = document.getElementById('w4-billing');
    var t = document.getElementById("target");
    var divtest = document.createElement("div");
    divtest.className = "form-group";
    divtest.innerHTML = t.innerHTML;
    objTo.appendChild(divtest);
    divtest.children[1].children[0].name = t.children[1].children[0].name + "" + count;
    divtest.children[2].children[0].name = t.children[2].children[0].name + "" + count;
    console.log(t.children[1].children[0].name);
    console.log(t.children[2].children[0].name);
    console.log(count);

  }
  else if(count==2){
    var objTo = document.getElementById('w4-billing');
    var divtest = document.createElement("div");   
    divtest.innerHTML = "<p style=\"color:red\">Only 3 rules can be attached </p>";
    objTo.appendChild(divtest);
    count++;

  }
  
}
(function ($) {

  'use strict';



	/*
	Wizard #4
  */


  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  var $w4finish = $('#w4').find('ul.pager li.finish'),
    $w4validator = $("#w4 form").validate({
      highlight: function (element) {
        $(element).closest('.form-group').removeClass('has-success').addClass('has-error');
      },
      success: function (element) {
        $(element).closest('.form-group').removeClass('has-error');
        $(element).remove();
      },
      errorPlacement: function (error, element) {
        element.parent().append(error);
      }
    });

  function setHeader(xhr) {

    xhr.setRequestHeader('Access-Control-Allow-Origin', "*");
  }

  $w4finish.on('click', function (ev) {
    ev.preventDefault();
    var validated = $('#w4 form').valid();
    if (validated) {
      //console.log($("#thing").serializeJSON())
      //console.log(formToJson($("thing")));
      var item = {};

      var splittedFormData = $("#thing").serialize().split('&');

      $.each(splittedFormData, function (key, value) {

        var splittedValue = value.split('=');
        item[splittedValue[0]] = splittedValue[1];
      });

      console.log(item);
      $.ajax({
        url: 'http://localhost:8000/api/create_thing/',
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        type: 'POST',
        data: JSON.stringify(item),
        datatype: 'jsonp',
        crossDomain: true,
        csrfmiddlewaretoken: getCookie('csrftoken'),
        beforeSend: function (xhr, settings) {
          xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: function (data) {
          console.log(data)
          new PNotify({
            title: 'Success!!',
            text: 'New thing Created Successfully!',
            type: 'custom',
            addclass: 'notification-success',
            icon: 'fa fa-check'
          });
        },
      });
    }
  });

  $('#w4').bootstrapWizard({
    tabClass: 'wizard-steps',
    nextSelector: 'ul.pager li.next',
    previousSelector: 'ul.pager li.previous',
    firstSelector: null,
    lastSelector: null,
    onNext: function (tab, navigation, index, newindex) {
      var validated = $('#w4 form').valid();
      if (!validated) {
        $w4validator.focusInvalid();
        return false;
      }
    },
    onTabClick: function (tab, navigation, index, newindex) {
      if (newindex == index + 1) {
        return this.onNext(tab, navigation, index, newindex);
      } else if (newindex > index + 1) {
        return false;
      } else {
        return true;
      }
    },
    onTabChange: function (tab, navigation, index, newindex) {
      var $total = navigation.find('li').size() - 1;
      $w4finish[newindex != $total ? 'addClass' : 'removeClass']('hidden');
      $('#w4').find(this.nextSelector)[newindex == $total ? 'addClass' : 'removeClass']('hidden');
    },
    onTabShow: function (tab, navigation, index) {
      var $total = navigation.find('li').length - 1;
      var $current = index;
      var $percent = Math.floor(($current / $total) * 100);
      $('#w4').find('.progress-indicator').css({ 'width': $percent + '%' });
      tab.prevAll().addClass('completed');
      tab.nextAll().removeClass('completed');
    }
  });


}).apply(this, [jQuery]);

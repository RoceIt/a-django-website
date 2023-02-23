// needs the js-cookie  jquery plugin

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
$(document).ajaxSend(function(event, jqxhr, settings) {
  if(!csrfSafeMethod(settings.type) && !this.crossDomain) {
    jqxhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
    }
});

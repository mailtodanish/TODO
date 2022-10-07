/* globals Chart:false, feather:false */

(function () {
  'use strict'
  feather.replace()
}())

window.onload = function() {
  var revison_ctx = document.getElementById('RevisionChart').getContext('2d');
  window.myPie = new Chart(revison_ctx, revision_config);
  var activity_ctx = document.getElementById('Activity').getContext('2d');
  window.myPie = new Chart(activity_ctx, activity_config);
};

$( ".chart_card" )
.mouseover(function() {
$(this).addClass("shadow-custom");
})
.mouseout(function() {
 $(this).removeClass("shadow-custom");
});


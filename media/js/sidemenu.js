jQuery(document).ready(function() {
  if(!$('.labs-sectionmenu').length) return false;

  var elt = jQuery('.menu-active');
  var currentIdx = parseInt(jQuery(elt).attr('data-depth'), 10);
  
  function initMenu() {
    jQuery(elt).show();
  }
  
  function showSibling(eltIdx) {
    var prev = eltIdx-1;
    var prevSibling = jQuery(elt).prevUntil('.menu-'+prev, '.menu-'+eltIdx);
    var nextSibling = jQuery(elt).nextUntil('.menu-'+prev, '.menu-'+eltIdx);
    prevSibling.show();
    nextSibling.show();
  }
  
  function showParent(eltIdx) {
    for (idx = eltIdx-1; idx >= 3; idx = idx-1) {
      var parentClassIdx = '.menu-'+ idx;
      var parent = jQuery(elt).prevAll(parentClassIdx).first();
      parent.show();
      showSibling(idx);
    }
  }
  
  function showChildren(eltIdx) {
    var next = eltIdx+1;
    var children = jQuery(elt).nextUntil('.menu-'+eltIdx, '.menu-'+next);
    children.show()
  }
  
  initMenu();
  showParent(currentIdx);
  showChildren(currentIdx);
  showSibling(currentIdx);
 
});

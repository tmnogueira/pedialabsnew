jQuery(document).ready(function() {
  if(!$('.labs-sectionmenu').length) return false;

  var elt = jQuery('.menu-active');
  var eltIdx = jQuery(elt).attr('data-depth');
  
  function initMenu() {
    jQuery(elt).show();
  }
  
  function showParent() {
    for (idx = eltIdx-1; idx >= 3; idx = idx-1) {
      var parentClassIdx = '.menu-'+ idx;
      var parent = jQuery(elt).prevAll(parentClassIdx).first();
      parent.show();
    }
  }
  
  function showSibling() {
    var prev = eltIdx-1;
    prevSibling = jQuery(elt).prevUntil('.menu-'+prev, '.menu-'+eltIdx);
    nextSibling = jQuery(elt).nextUntil('.menu-'+prev, '.menu-'+eltIdx);
    prevSibling.show();
    nextSibling.show();
  }
  
  function showChildren() {
    var next = eltIdx+1;
    var children = jQuery(elt).nextUntil('.menu-'+next, '.menu-'+eltIdx);
    children.show()
  }
  
  initMenu();
  showParent();
  showChildren();
  showSibling();
 
});

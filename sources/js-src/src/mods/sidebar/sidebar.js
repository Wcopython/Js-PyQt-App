import "./sidebar-menu.css";
$.sidebarMenu = function(menu) {
  var animationSpeed = 100;
  
  $(menu).on('click', 'li a', function(e) {
    var $this = $(this);
    var checkElement = $this.next();

    if (checkElement.is('.treeview-menu') && checkElement.is(':visible')) {
      checkElement.slideUp(animationSpeed, function() {
        checkElement.removeClass('menu-open');
      });
      checkElement.parent("li").removeClass("active");
    }

    //If the menu is not visible
    else if ((checkElement.is('.treeview-menu')) && (!checkElement.is(':visible'))) {
      //Get the parent menu
      var parent = $this.parents('ul').first();
      //Close all open menus within the parent
      var ul = parent.find('ul:visible').slideUp(animationSpeed);
      //Remove the menu-open class from the parent
      ul.removeClass('menu-open');
      //Get the parent li
      var parent_li = $this.parent("li");

      //Open the target menu and add the menu-open class
      checkElement.slideDown(animationSpeed, function() {
        //Add the class active to the parent li
        checkElement.addClass('menu-open');
        parent.find('li.active').removeClass('active');
        parent_li.addClass('active');
      });
    }
    else{
      var parent = $this.parents('ul').first();
      //Close all open menus within the parent
      var ul = parent.find('ul:visible').slideUp(animationSpeed);
      //Remove the menu-open class from the parent
      ul.removeClass('menu-open');
      //Get the parent li
      parent.find('li.active').removeClass('active');
      $this.parent("li").addClass('active');

    }
    //if this isn't a link, prevent the page from being redirected
    if (checkElement.is('.treeview-menu')) {
      e.preventDefault();
    }
  });
}

export default{
  toggle:function(){
      var $side = $('.main-sidebar'),
          showing = $side.css("left")=='0px';
      $side.animate({ "left": showing?"-230px":"0px"},50);
      $(".chapter").animate({ "margin-left": showing?"0":"230px"},50);
      $(".sidebar-flag .fa").attr("class","fa fa-angle-"+(showing?"right":"left"));
      window.event.stopPropagation();
  },
  init:function(selector){
      $.sidebarMenu(selector);
      $(".chapter").click(function(){
          $('.main-sidebar').animate({ "left": "-230px"},50);
          $(".chapter").animate({ "margin-left": "0"},50);
          $(".sidebar-flag .fa").attr("class","fa fa-angle-right");
      });
  }
}

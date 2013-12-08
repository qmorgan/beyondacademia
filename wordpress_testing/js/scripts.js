/**************************************************************/
/* Prepares the cv to be dynamically expandable/collapsible   */
/**************************************************************/
function prepareList() {
    //does the list item have child unordered list? if so, 
    // allow it to be expanded
    $('#expList').find('li:has(ul)') 
    .click( function(event) {
        // Removed the below and changed it to always true since
        // it was not allowing nested tags like <b> and <p> from
        // triggering the expand/collapse event.. -amorgan
        // Changed it to allow for expand/collapse on any tag
        // except for stuff in the NOCLICK tag.
        // if (this == event.target)
        if (event.target.nodeName !== "NOCLICK") {
            $(this).toggleClass('expanded');
            $(this).children('ul').toggle('medium');
        }
        return false;
    })
    

    
    .addClass('collapsed')
    .children('ul').hide();

    //Create the button funtionality
    $('#expandList')
    .unbind('click')
    .click( function() {
        $('.collapsed').addClass('expanded');
        $('.collapsed').children('ul').show('medium');
    })
    $('#collapseList')
    .unbind('click')
    .click( function() {
        $('.collapsed').removeClass('expanded');
        $('.collapsed').children('ul').hide('medium');
    })
    
};


/**************************************************************/
/* Functions to execute on loading the document               */
/* Need to call it this way, not using $, for worpress        */
/**************************************************************/
jQuery(document).ready(function(){
    jQuery(prepareList())
});
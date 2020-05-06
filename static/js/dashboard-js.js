(function($){
	$(document).ready(function(){

		/* Create checkbox/toggle UI based off form data */

		$("div.et_social_multi_selectable").click(function() {
			var checkbox = $(this).children("input");
			if ($(checkbox).val() == "on") {
				$(checkbox).val("off");
			} else {
				$(checkbox).val("on");
			}
			$(this).toggleClass( "et_social_selected et_social_just_selected" );
			$(this).mouseleave(function() {
			 	$(this).removeClass( "et_social_just_selected" );
			});
		});

		$("div.et_social_single_selectable").click(function() {
			var tabs = $(this).parents(".et_social_row").find("div.et_social_single_selectable");
			var inputs = $(this).parents(".et_social_row").find("input");
			tabs.removeClass( "et_social_selected" );
			inputs.val("off");
			$(this).toggleClass( "et_social_selected" )
			$(this).children("input").val("on")
		});

		function toggle() {
			$(this).parent().addClass("et_social_selected");
		}

		$("input.et_social_toggle[value='on']").each(toggle);

		/* Tabs System */

		$("div#et_social_navigation > ul > li > a").click(function() {
			var button = $(this).parent().find("ul > li > a").first().attr("id");
		    var tab = $("div." + button);
		    var current = $("a.current");
		    var current_section = $("ul.current_section");
			current_section.removeClass("current_section");
			$(this).next().toggleClass("current_section");
		    $(current).removeClass("current");
		    $(this).parent().find("ul > li > a").first().addClass("current");
		    $("div.et_social_tab_content").removeClass( "et_tab_selected" );
		    $(tab).addClass("et_tab_selected");
		});

		$("div#et_social_header > ul > li > a").click(function() {
			var button = $(this).attr("id");
		    var tab = $("div." + button);
		    var current = $("a.current");
		    var current_section = $("ul.current_section");
			current_section.removeClass("current_section");
		    $(current).removeClass("current");
		    $(this).addClass("current");
		    $("div.et_social_tab_content").removeClass( "et_tab_selected" );
		    $(tab).addClass("et_tab_selected");
		});

		$("#et_social_navigation ul li ul li > a").click(function() {
		    var button = $(this).attr("id");
		    var tab = $("div." + button);
		    var current = $("a.current");
		    $(current).removeClass("current");
		    $(this).addClass("current");
		    $("div.et_social_tab_content").removeClass("et_tab_selected");
		    $(tab).addClass("et_tab_selected");
		});

		/* Build a uniform statistics graph based on data input*/

		function resize() {
			var bar_array = $(".et_social_tab_content_stats ul li > div").map(function() {
	  			return $(this).attr("value");
			}).get();
			var bar_height = Math.max.apply(Math, bar_array);

			var value = $(this).attr("value");
			var li_height = value / bar_height * 300;
			$(this).height(li_height);
		}

		$(".et_social_graph li div > div").hover(function() {
			var value = $(this).attr("value");
			var type = $(this).attr("type");
			$(this).append("<div class='et_social_tooltip'><strong>"+type+"</strong><br>Shares: "+value+"</div>");
		}, function() {
			$(this).find("div.et_social_tooltip").remove();
		});

		function resize_network() {
			var value = $(this).attr("value");
			var parent_value = $(this).parent().attr("value");
			var new_height = value / parent_value * 100;
			var percentage = new_height + "%";
			var type = $(this).attr("type");
			$(this).css("height", percentage);
			$(this).addClass("et_social_" + type)
		}

		$(".et_social_tab_content_stats ul li > div").each(resize);
		$(".et_social_tab_content_stats ul li > div > div").each(resize_network);

		/* jQuery Sortable */

		$(function() {
		    $( ".et_social_sortable" ).sortable({
		      placeholder: "et_social_sortable_placeholder"
		    });
		    $( ".et_social_sortable" ).disableSelection();
		 });

    });
})(jQuery)
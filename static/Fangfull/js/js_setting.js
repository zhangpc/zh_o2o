/**
 * Created by Administrator on 2016/12/2.
 */

$.ajaxSetup({cache: false});
jQuery.get('/Fangfull/chiocesetting',
    function(data_message){
        var indexid = 1;
        jQuery.get("/static/tmpl/tmpl_settings.html", function(data, textStatus, XMLHttpRequest){
            $.tmpl(data,{address_message:data_message.message_url}).appendTo( "#table_set_list" );});
})
function selectContent(index) {
    index = index+1;
    jQuery.get('/Fangfull/chiocesetting',{'indexid':index},function(data){
        $('#url_blue').html("");
        $('#url_red').html("");
        for ( var i=0; i < data.message_url['url_blue'].length; i ++){
            $('#url_blue').append("<option>"+data.message_url['url_blue'][i] +"</option>");
            $('#url_red').append("<option>"+data.message_url['url_red'][i] +"</option>");
        }
    })
}
$(function() {
    $(document).on("change", "#sql_name", function(){
        var sql_name = $(this).find("option:selected").index()+1;
    })
    $(document).on("change", "#url_blue", function(){
        var url_blue = $(this).find("option:selected").index()+1;
    })
});


        //
        //$("#sql_name").get(0).selectedIndex=1
        //debugger;
        //$("#sql_name").change(function(){
        //    alert(1);
        //})
        //
        //$('#siteurl').change(function(){
        //    siteurl = $('#siteurl').val();
        //    dictcontext = {'siteurl':siteurl}
        //    jQuery.get($SCRIPT_ROOT+'/Fangfull/chiocesetting',
        //    dictcontext,
        //    function(data_message){
        //        $("#ipbule").html("");
        //        $("#ipred").html("");
        //        jQuery.get("/static/tmpl/tmpl_settings.html", function(data, textStatus, XMLHttpRequest){
        //         address_message = {'url_blue':url_blue,'url_red':url_red,'sql_id':sql_id,'url_id':url_id}
        //            $.tmpl(data,{address_message:data_message.address_message}).appendTo( "#ipbule" );
        //            $.tmpl(data,{address_message:data_message.address_message}).appendTo( "#ipred" );
        //        });
        //    })
        //});
        //$('#save').click(function(){
        //    var ip_bule = $('#ipbule').val();
        //    var ip_red = $('#ipred').val();
        //    var content_sql = $('#contentsql').val();
        //    dictcontext = {
        //                    'ip_bule':ip_bule,
        //                    'ip_red':ip_red,
        //                    'content_sql':content_sql}
        //    jQuery.get($SCRIPT_ROOT+'/Fangfull/setBasics',
        //        dictcontext,
        //        function(basics_mssage){
        //            $('#result').text(basics_mssage['ipblue']);
        //            }
        //        );
        //});
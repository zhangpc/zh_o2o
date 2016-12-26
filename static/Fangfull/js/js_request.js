
$.ajaxSetup ({ cache: false });
jQuery.get('/Fangfull/getMessageRes',
    function(message_res){
        var reslist_index;
        var reslist;
        var res_id;
        var datalist;
        var dataModel;

        jQuery.get("/static/tmpl/tmpl_request.html", function(data, textStatus, XMLHttpRequest){
        //{{if messageres.res_id[$index] == messagedata.res_id[$index]}}
            $.tmpl(data,{messageres:message_res.MessageRes}).appendTo( "#message_res" );
            $('#message_res tr a.submit').click(function(){
                alert($(this).attr("id"));
                var res_id = $("res_id").val();
                var data_id = $("data_id").val();
                var data_value = $("data_name3").val();
                alert(res_id);
                alert(data_id);
                alert(data_value);
                jQuery.get('/Fangfull/postMessageData',{'res_id':res_id,'data_id':data_id,'data_value':data_value},
                function(data){
                });
            });

        });
})

function message_res(parant){
    detail_a = $(parant).attr('id');
    reslist_tr_index = $(parant).parents().parents().attr('index');
    dataModel_isDisplay =  "#dataModel"+String(reslist_tr_index);
    datalist = ".datalist"+String(reslist_tr_index);
    var res_id = String(reslist_tr_index);
    if ($(dataModel_isDisplay).css("display")=="none"){
        jQuery.get('/Fangfull/getMessageData',{'res_id':String(res_id)},
        function(message_data){
            $(datalist).html("");
            jQuery.get("/static/tmpl/tmpl_request_data.html", function(data1, textStatus, XMLHttpRequest){
                $(dataModel_isDisplay).css("display","table-row");
                $.tmpl(data1,{messagedata:message_data.MessageData}).appendTo( datalist );
                //$(".save").click(function(){
                //    alert($($(this).parents('tr')[0]).find(".data_id").val());
                //});
            })
        })
    }
    else {
        $(dataModel_isDisplay).css("display", "none");
    }
}
//,data_name,data_value,data_describe
function save_data(data){
    var trList = $(data).parents().parents().attr('id');
    $("#"+trList).each(function(){
        tdArr = $(this).children();
        data_id = tdArr.eq(0).find("label").val();
        data_name = tdArr.eq(1).find("input").val();
        data_value = tdArr.eq(2).find("input").val();
        data_describe = tdArr.eq(3).find("input").val();
    });
    jQuery.get("/Fangfull/postMessageData",
            {'data_id':data_id,
            'data_name':data_name,
            'data_value':data_value,
            'data_describe':data_describe},
            function(data){
                alert(data.MessageData);
            }
    );
}
function new_data(btn){
    alert($(btn).parents().parents().index());
}

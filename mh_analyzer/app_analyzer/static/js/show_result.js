'use strict';



function change_to(state){
    var childs = document.getElementById("main_div").childNodes;
    var in_main_div = function (id){
        switch(id){
            case "analyzer":
            case "comparer":
            case "fast_analyzer":
                return true;
            default:
                return false;
        }
    }
    for (var i = 0; i < childs.length; i++){
        if(in_main_div(childs[i].id)){
            childs[i].style.display = 'none';
        }
    }
    document.getElementById(state).style.display = "block";
}

function add_cmp_form_line(attr_name, attr_cn_name, form_id, value, delta_value){
    let cmp_form = document.getElementById("cmp_form");
    let sub_form = document.getElementById(form_id);

    let submit_btn = document.getElementById("cmp_form_submit");
    if (submit_btn != null){
        cmp_form.removeChild(submit_btn); 
    }
    submit_btn = document.createElement("button");
    submit_btn.className = "btn btn-primary btn-lg btn-block";
    submit_btn.id = "cmp_form_submit";
    submit_btn.innerHTML = "提交";

    let form_line_div = document.createElement("div");
    form_line_div.className = "form-group";

    let _label1 = document.createElement("label");
    _label1.className = "col-sm-1";
    form_line_div.appendChild(_label1);

    let _label2 = document.createElement("label");
    _label2.className = "col-sm-4";
    _label2.innerHTML = attr_cn_name;
    form_line_div.appendChild(_label2)

    let _label3 = document.createElement("label");
    _label3.className = "col-sm-1";
    _label3.innerHTML = value;
    form_line_div.appendChild(_label3)

    let _label4 = document.createElement("label");
    _label4.className = "col-sm-1";
    _label4.innerHTML = "+";
    form_line_div.appendChild(_label4)

    let inner_div1 = document.createElement("div");
    let _input1 = document.createElement("input");
    _input1.type = "text";
    _input1.className = "col-sm-2";
    if (form_id == "cmp_form_left"){
        _input1.name = attr_name + '_l';
    }else if(form_id == "cmp_form_right"){
        _input1.name = attr_name + '_r';
    }
    _input1.value = delta_value;
    inner_div1.appendChild(_input1);
    form_line_div.appendChild(inner_div1);
    
    sub_form.appendChild(form_line_div);
    cmp_form.appendChild(submit_btn);
}

function delete_sub_form_line(form_id){
    let sub_form = document.getElementById(form_id)
    let lines = sub_form.childNodes
    if( lines.length > 0){
        sub_form.removeChild(lines[lines.length - 1]);
    }
    

    let cmp_form_left = document.getElementById("cmp_form_left");
    let cmp_form_right = document.getElementById("cmp_form_right");
    if ((cmp_form_left.childNodes.length == 0) && (cmp_form_right.childNodes.length == 0)){
        let cmp_form = document.getElementById("cmp_form");
        let submit_btn = document.getElementById("cmp_form_submit");
        cmp_form.removeChild(submit_btn);
    }
}
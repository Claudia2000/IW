
$(function()
{

$("#myTable").on('click','.delete',function(){    

    var currentRow=$(this).closest("tr");
    var col1=currentRow.find("td:eq(0)").text(); // get current row 1st TD value
    $.ajax({
        type: "POST",
        url:'http://127.0.0.1:5000/delete_cliente/'+col1,
        success: function(){
            alert("Se eliminó correctamente");
        }
    })
})

$("#myTable").on('click','.update',function(){    
    
    var currentRow=$(this).closest("tr");
    var col1=currentRow.find("td:eq(0)").text();
    var col2=currentRow.find("td:eq(1)").text(); 
    var col3=currentRow.find("td:eq(2)").text(); 
    var col4=currentRow.find("td:eq(3)").text();
    $.ajax({
        type: "POST",
        url:'http://127.0.0.1:5000/update_cliente/'+col1,
        data:JSON.stringify({
            "name":col2,
            "dni":col3,
            "cel":col4
        }),
        contentType: "application/json; charset=utf-8",
        traditional: true,
        success: function(){
            alert("se actualizo correctamente");
        }
    })
})
$('#create').click(function(){
    var valor = document.getElementById("name").value;
    var valor2 = document.getElementById("dni").value;
    var valor3 = document.getElementById("cel").value;

    $.ajax({
        type: "POST",
        url:'http://127.0.0.1:5000/create_cliente',
        data:JSON.stringify({
            "name":valor,
            "dni":valor2,
            "cel":valor3
        }),
        contentType: "application/json; charset=utf-8",
        traditional: true,
        success: function(){
            alert("se ingreso correctamente");
        }
    })
    
})

$('#createres').click(function(){
    var valor = document.getElementById("nomcli").value;
    var valor1 = document.getElementById("fecha_ingreso").value;
    var valor2 = document.getElementById("fecha_salida").value;

    $.ajax({
        type: "POST",
        url:'http://127.0.0.1:5000/create_reserva',
        data:JSON.stringify({
            "nomcli":valor,
            "fecha_ingreso":valor1,
            "fecha_salida":valor2
        }),
        contentType: "application/json; charset=utf-8",
        traditional: true,
        success: function(){
            alert("Se ingresó correctamente");
        }
    })
    
})

}


)
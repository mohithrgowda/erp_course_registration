$("#attupdate_btnsubmit").click(function(){
	debugger;
   var form_data = new FormData($('#atupdate')[0]);
   if(form_data.get('sst')=="")
				{
					alert('Shift Not Assigned');
				}
				else{
        $.ajax({
            type: 'POST',
            url: '/updateattendance',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                console.log(data);
				alert('Attendance updated successfully');
				
				window.location='hrattendance';
            },
        });
	}
});



$("#btn_login").click(function(){
	debugger;
	var uname=document.getElementById('name').value;
	var pswd=document.getElementById('passwrd').value;
	if(uname=="admin" && pswd=="admin")
	{
		window.location="adminhome";
	}
	else 
	 {
		
	$.ajax({
            type: 'GET',
            url: '/logdata',
			
        contentType: 'application/json;charset=UTF-8',
            data: {
            'name': uname,
            'passwrd': pswd
			

        },
            
        dataType:"json",
            success: function(data) {
				alert(data);
				if(data=="Failure")
				{
					alert("Credentials not found");
					window.location='login';
				}
				if(data=="Student")
				{
					alert('Logged in Successfully');
				   window.location='studenthome';
				}
				if(data=="Mentor")
				{
					alert('Logged in Successfully');
				   window.location='mentorhome';
				}
				if(data=="HOD")
				{
					alert('Logged in Successfully');
				   window.location='hodhome';
				}
            },
			 error: function(data) {
               alert (data.responseText);
            }
        });
	}
		
	
});



//HR Attendance Empcode wise Search
$("#btn_searchempcode").click(function(){		
		debugger;
		var secode=document.getElementById('secode').value;
		window.location='srchhrattendance?secode='+secode;
});	

//HR Attendance Process wise Search
$("#btn_searchbyproc").click(function(){		
		debugger;
		var procnm=document.getElementById('procnm').value;
		window.location='srchbyproc?procnm='+procnm;
});		



//HR Attendance Manager wise Search
$("#btn_searchbymgr").click(function(){		
		debugger;
		var mgrnm=document.getElementById('mgrnm').value;
		window.location='srchbymgr?mgrnm='+mgrnm;
});	


//HR Attendance Search
$("#btn_searchalldata").click(function(){		
		debugger;
		var secode=document.getElementById('secode').value;
		var procnm=document.getElementById('procnm').value;
		var mgrnm=document.getElementById('mgrnm').value;
		var mon=document.getElementById('mon').value;
		var year=document.getElementById('year').value;
		window.location='srchhrattendance?month='+mon+'&year='+year+'&secode='+secode+'&procnm='+procnm+'&mgrnm='+mgrnm;
});	

//HR Attendance Search
$("#btn_updatepayroll").click(function(){		
	debugger;
	var mon=document.getElementById('mon').value;
	var year=document.getElementById('year').value;
	$.ajax({
		type: 'GET',
		url: '/updatepayroll',
		
	contentType: 'application/json;charset=UTF-8',
		data: {
		'month': mon,
		'year': year
		},
		beforeSend: function () {
			showmodal()
		 },
		 complete: function () {
			 $(".modall").hide();
		 },
		
	dataType:"json",
		success: function(data) {
			alert(data);
		},
		 error: function(data) {
		   
		}
	});
});	

function showmodal()
{
	debugger;
	$(".modall").show();
}

function fetchmondata()
{
	debugger;
	var mon=document.getElementById('mon').value;
	var year=document.getElementById('year').value;
	window.location='hrattendance1?month='+mon+'&year='+year;
	/*
	if(document.getElementById('mon').value=='12')
		window.location='hrattendance1?month=Dec&year=2021';
	else if(document.getElementById('mon').value=='1')
		window.location='hrattendance1?month=Jan&year=2022';
	else
		window.location='hrattendance?month=Feb&year=2022';
	*/
}

//Excel icon click
$("#btn_downloadexcel").click(function(){		
		debugger;
		var secode=document.getElementById('secode').value;
		var procnm=document.getElementById('procnm').value;
		var mgrnm=document.getElementById('mgrnm').value;
		var mon=document.getElementById('mon').value;
		var year=document.getElementById('year').value;
		console.log('exceldownload?month='+mon+'&year='+year+'&secode='+secode+'&procnm='+procnm+'&mgrnm='+mgrnm);
		window.location='exceldownload?month='+mon+'&year='+year+'&secode='+secode+'&procnm='+procnm+'&mgrnm='+mgrnm;
		var m=0;
});	


//Onboarding Creating New Employee
$("#btn_createemp").click(function(){
	debugger;
	var newename=document.getElementById('newename').value;
	if(newename=="")
	{
		alert("Please enter the employee name");
	}
	else{
	window.location='createnewemp?empname='+newename;
	}
	
	
});

$("#process").change(function () {
	debugger;
	var processval = this.value;
	$.ajax({
		type: 'GET',
		url: '/load_mgr_amgr',
		
	contentType: 'application/json;charset=UTF-8',
		data: {
		'process': processval
		},
		
	dataType:"json",
		success: function(data) {
			var dataarray = data.split("#");
			$('#mgrnm').empty();
			$('#amgrnm').empty();
			for(var m=0;m<dataarray.length-1;m++)
			{
				var rowdata=dataarray[m];
				var rowdataarray = rowdata.split(",");
				var newOption = $('<option>'+rowdataarray[0]+'</option>');
 				$('#mgrnm').append(newOption);
				 var newOption1 = $('<option>'+rowdataarray[1]+'</option>');
				  $('#amgrnm').append(newOption1);
			}
		},
		 error: function(data) {
		   
		}
	});
});


//Onboarding Search Employee
$("#btn_searchemp").click(function(){
	debugger;
	var empid=document.getElementById('empid').value;
	var ename=document.getElementById('ename').value;
	var edob=document.getElementById('edob').value;
	var ephone=document.getElementById('ephone').value;
	var procnm=document.getElementById('procnm').value;
	var estatus=document.getElementById('estatus').value;
       $.ajax({
            type: 'GET',
            url: '/searchonboardemp',
			
        contentType: 'application/json;charset=UTF-8',
            data: {
            'empid': empid,
            'ename': ename,
            'edob': edob,
            'ephone': ephone,
            'procnm': procnm,
			'estatus':estatus
			},
            
        dataType:"json",
            success: function(data) {
				//alert(data);
				document.getElementById("tblData").innerHTML="";
				
				var table = document.getElementById("tblData");	
				var header = table.createTHead();
				header.className="bg-darkblue text-white border-darkblue";
				
				var row = header.insertRow(0);
				var cell = row.insertCell(0);
				cell.innerHTML = "<b>Emp Code</b>";
				cell = row.insertCell(1);
				cell.innerHTML = "<b>Employee Name</b>";
				cell = row.insertCell(2);
				cell.innerHTML = "<b>Date Of Birth</b>";
				cell = row.insertCell(3);
				cell.innerHTML = "<b>Email</b>";
				cell = row.insertCell(4);
				cell.innerHTML = "<b>Mobile</b>";
				cell = row.insertCell(5);
				cell.innerHTML = "<b>View</b>";
				
				addEmpRow(data,'tblData');
            },
			 error: function(data) {
               
            }
        });
});


function addEmpRow(data,tableID) {  
	debugger;
	var table = document.getElementById(tableID);  
	var body = table.createTBody();
	var dataarray = data.split("#");
	for(var m=0;m<dataarray.length-1;m++)
	{
		var rowdata=dataarray[m];
		var rowdataarray = rowdata.split(",");
		 
		var rowCount =0;// table.rows.length;  
		var row = body.insertRow(rowCount);
		//for(var n=0;n<rowdataarray.length;n++)
		{
		 
			//Column 1  
			var cell1 = row.insertCell(0); 
			cell1.innerHTML = rowdataarray[0]; 
			
			//Column 2  
			var cell2 = row.insertCell(1); 
			cell2.innerHTML = rowdataarray[1]; 
			
			//Column 3  
			var cell3 = row.insertCell(2); 
			cell3.innerHTML = rowdataarray[2]; 
			
			//Column 4  
			var cell4 = row.insertCell(3); 
			cell4.innerHTML = rowdataarray[3]; 
			//Column 5 
			var cell4 = row.insertCell(4); 
			cell4.innerHTML = rowdataarray[4]; 
			//Column 5 
			var cell5 = row.insertCell(5); 
			cell5.innerHTML = "<a href='seeverempdata?empcode="+rowdataarray[5]+"' target='_blank'> <i class='fa fa-eye' aria-hidden='true'></i></a>"; 
			
			
			
			
			
		}
	}
	
	 
}

//Upload Qual File onboarding
$("#btn_addcertletter").click(function(){
	debugger;
   var form_data = new FormData($('#upload-file')[0]);
        $.ajax({
            type: 'POST',
            url: '/addcertfile',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                console.log('Success!');
				
				if(data!="")
				{
					document.getElementById('expcerttablediv').style.display="block";
					document.getElementById("expcerttable").innerHTML="";
					var table = document.getElementById("expcerttable");					
					var header = table.createTHead();
					var row = header.insertRow(0);
					var cell = row.insertCell(0);
					cell.innerHTML = "<b>Company</b>";
					cell = row.insertCell(1);
					cell.innerHTML = "<b>From</b>";
					cell = row.insertCell(2);
					cell.innerHTML = "<b>To</b>";
					cell = row.insertCell(3);
					cell.innerHTML = "<b>Designation</b>";
					cell = row.insertCell(4);
					cell.innerHTML = "<b>Certificate</b>";
					cell = row.insertCell(5);
					cell.innerHTML = "<b>View</b>";
					cell = row.insertCell(6);
					cell.innerHTML = "<b>Delete</b>";
					data=data.replace("\"","");	
					data=data.substr(0,data.length-2);
					addRowExpCert('expcerttable',data,'tblonboardingexpcert','CertFile');
					//alert(data);
				}
            },
        });

});


//Upload Qual File onboarding
$("#btn_addqual").click(function(){
	debugger;
   var form_data = new FormData($('#upload-file')[0]);
        $.ajax({
            type: 'POST',
            url: '/addqualfile',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                console.log('Success!');
				
				if(data!="")
				{
					document.getElementById('qualtablediv').style.display="block";
					document.getElementById("qualtable").innerHTML="";
					var table = document.getElementById("qualtable");					
					var header = table.createTHead();
					var row = header.insertRow(0);
					var cell = row.insertCell(0);
					cell.innerHTML = "<b>Qualification</b>";
					cell = row.insertCell(1);
					cell.innerHTML = "<b>Document</b>";
					cell = row.insertCell(2);
					cell.innerHTML = "<b>View</b>";
					cell = row.insertCell(3);
					cell.innerHTML = "<b>Delete</b>";
					data=data.replace("\"","");	
					data=data.substr(0,data.length-2);
					addRow('qualtable',data,'tblonboardingqual','QualFile');
					//alert(data);
				}
            },
			error: function(data) {
				alert(data);
               
            }
        });

});

//Upload Qual File onboarding
$("#btn_addqualx").click(function(){
	debugger;
   var form_data = new FormData($('#uploadqualfile')[0]);
        $.ajax({
            type: 'POST',
            url: '/addqualfile',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                console.log('Success!');
				
				if(data!="")
				{
					document.getElementById('qualtablediv').style.display="block";
					document.getElementById("qualtable").innerHTML="";
					var table = document.getElementById("qualtable");					
					var header = table.createTHead();
					var row = header.insertRow(0);
					var cell = row.insertCell(0);
					cell.innerHTML = "<b>Qualification</b>";
					cell = row.insertCell(1);
					cell.innerHTML = "<b>Document</b>";
					cell = row.insertCell(2);
					cell.innerHTML = "<b>View</b>";
					cell = row.insertCell(3);
					cell.innerHTML = "<b>Delete</b>";
					data=data.replace("\"","");	
					data=data.substr(0,data.length-2);
					addRow('qualtable',data,'tblonboardingqual','QualFile');
					//alert(data);
				}
            },
			error: function(data) {
				alert(data);
               
            }
        });

});


$("#btn_addidcard").click(function(){
	debugger;
   var form_data = new FormData($('#upload-file')[0]);
        $.ajax({
            type: 'POST',
            url: '/addidcard',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                console.log('Success!');
				
				if(data!="")
				{
					document.getElementById('idcardtablediv').style.display="block";
					document.getElementById("idcardtable").innerHTML="";
					var table = document.getElementById("idcardtable");					
					var header = table.createTHead();
					var row = header.insertRow(0);
					var cell = row.insertCell(0);
					cell.innerHTML = "<b>Id Card</b>";
					cell = row.insertCell(1);
					cell.innerHTML = "<b>Document</b>";
					cell = row.insertCell(2);
					cell.innerHTML = "<b>View</b>";
					cell = row.insertCell(3);
					cell.innerHTML = "<b>Delete</b>";
					data=data.replace("\"","");	
					data=data.substr(0,data.length-2);
					addRow('idcardtable',data,'tblonboardingidcard','IdCards');
					//alert(data);
				}
            },
        });

});

$("#btn_addcovidreport").click(function(){
	debugger;
   var form_data = new FormData($('#upload-file')[0]);
        $.ajax({
            type: 'POST',
            url: '/addcovidrep',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                console.log('Success!');
				
				if(data!="")
				{
					document.getElementById('covidreptablediv').style.display="block";
					document.getElementById("covidreptable").innerHTML="";
					var table = document.getElementById("covidreptable");					
					var header = table.createTHead();
					var row = header.insertRow(0);
					var cell = row.insertCell(0);
					cell.innerHTML = "<b>Vaccination</b>";
					cell = row.insertCell(1);
					cell.innerHTML = "<b>Document</b>";
					cell = row.insertCell(2);
					cell.innerHTML = "<b>View</b>";
					cell = row.insertCell(3);
					cell.innerHTML = "<b>Delete</b>";
					data=data.replace("\"","");	
					data=data.substr(0,data.length-2);
					addRow('covidreptable',data,'tblonboardingcovidrep','CovidReports');
					//alert(data);
				}
            },
        });

});



$("#btn_addscanletter").click(function(){
	debugger;
   var form_data = new FormData($('#upload-file')[0]);
        $.ajax({
            type: 'POST',
            url: '/addscandoc',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                console.log('Success!');
				
				if(data!="")
				{
					document.getElementById('scanlettertablediv').style.display="block";
					document.getElementById("scanlettertable").innerHTML="";
					var table = document.getElementById("scanlettertable");					
					var header = table.createTHead();
					var row = header.insertRow(0);
					var cell = row.insertCell(0);
					cell.innerHTML = "<b>Id Card</b>";
					cell = row.insertCell(1);
					cell.innerHTML = "<b>Document</b>";
					cell = row.insertCell(2);
					cell.innerHTML = "<b>Company Order</b>";
					cell = row.insertCell(3);
					cell.innerHTML = "<b>View</b>";
					cell = row.insertCell(4);
					cell.innerHTML = "<b>Delete</b>";
					data=data.replace("\"","");	
					data=data.substr(0,data.length-2);
					addRowScanDoc('scanlettertable',data,'tblonboardingscandoc','ScanDoc');
					//alert(data);
				}
            },
        });

});



function addRowScanDoc(tableID,data,tblname,foldername) {  
	debugger;
		
	var table = document.getElementById(tableID);  
	
	var body = table.createTBody();
	var dataarray = data.split("#");
	for(var m=0;m<dataarray.length;m++)
	{
		var rowdata=dataarray[m];
		var rowdataarray = rowdata.split(",");
		 
		var rowCount = 0;//table.rows.length;  
		var row = body.insertRow(rowCount);
		//for(var n=0;n<rowdataarray.length;n++)
		{
		 
			//Column 1  
			var cell1 = row.insertCell(0); 
			cell1.innerHTML = rowdataarray[1]; 
			
			//Column 2  
			var cell2 = row.insertCell(1); 
			cell2.innerHTML = rowdataarray[2]; 
			
			//Column 3  
			var cell3 = row.insertCell(2); 
			cell3.innerHTML = rowdataarray[3]; 
			
			//Column 4  
			var cell4 = row.insertCell(3); 
			cell4.innerHTML = "<a href='./static/"+foldername+"/"+rowdataarray[2]+"' target='_blank'> <i class='fa fa-eye' aria-hidden='true'></i></a>"; 
			
			
			//Column 5 
			var cell5 = row.insertCell(4); 
			cell5.innerHTML = "<a onclick='deletefile("+rowdataarray[0]+",\""+tblname+"\")'> <i class='fa fa-trash' aria-hidden='true'></i></a>"; 
			
			
		}
	}
	
	 
}

function addRow(tableID,data,tblname,foldername) {  
	debugger;
		
	var table = document.getElementById(tableID);  
	
	var body = table.createTBody();
	var dataarray = data.split("#");
	for(var m=0;m<dataarray.length;m++)
	{
		var rowdata=dataarray[m];
		var rowdataarray = rowdata.split(",");
		 
		var rowCount =0;// table.rows.length;  
		//var row = table.insertRow(rowCount);
		var row = body.insertRow(rowCount);
		//for(var n=0;n<rowdataarray.length;n++)
		{
		 
			//Column 1  
			var cell1 = row.insertCell(0); 
			cell1.innerHTML = rowdataarray[1]; 
			
			//Column 2  
			var cell2 = row.insertCell(1); 
			cell2.innerHTML = rowdataarray[2]; 
			
			//Column 3  
			var cell3 = row.insertCell(2); 
			cell3.innerHTML = "<a href='./static/"+foldername+"/"+rowdataarray[2]+"' target='_blank'> <i class='fa fa-eye' aria-hidden='true'></i></a>"; 
			/*
			//Column 4 			
			var cell4 = row.insertCell(3); 
			var element1 = document.createElement("input");  
			element1.type = "button";  
			var btnName = "button" + (rowCount + 1);  
			element1.name = btnName;  
			element1.setAttribute('value', 'Delete'); // or element1.value = "button";  
			element1.onclick = function() {  
				removeRow(btnName);  
			}  
			cell4.appendChild(element1);  
			*/
			
			//Column 4 
			var cell4 = row.insertCell(3); 
			//cell4.innerHTML = "<a href='delfile?id="+rowdataarray[0]+"&tblname="+tblname+"'> <i class='fa fa-trash' aria-hidden='true'></i></a>"; 
			cell4.innerHTML = "<a onclick='deletefile("+rowdataarray[0]+",\""+tblname+"\")'> <i class='fa fa-trash' aria-hidden='true'></i></a>"; 
			
			
			/*
			 
			var element1 = document.createElement("input");  
			element1.type = "button";  
			var btnName = "button" + (rowCount + 1);  
			element1.name = btnName;  
			element1.setAttribute('value', 'Delete'); // or element1.value = "button";  
			element1.onclick = function() {  
				removeRow(btnName);  
			}  
			cell1.appendChild(element1);  
			
			//Column 2 
			var cell2 = row.insertCell(1);  
			cell2.innerHTML = rowCount + 1;  
			
			//Column 3  
			var cell3 = row.insertCell(2);  
			var element3 = document.createElement("input");  
			element3.type = "text";  
			cell3.appendChild(element3);
			
			//Column 4  
			var cell3 = row.insertCell(2);  
			var element3 = document.createElement("input");  
			element3.type = "text";  
			cell3.appendChild(element3);  
			*/
		}
	}
	
	 
}



function addRowExpCert(tableID,data,tblname,foldername) {  
	debugger;
		
	var table = document.getElementById(tableID);  
	var body=table.createTBody();
	var dataarray = data.split("#");
	for(var m=0;m<dataarray.length;m++)
	{
		var rowdata=dataarray[m];
		var rowdataarray = rowdata.split(",");
		 
		var rowCount = 0;//table.rows.length;  
		var row = body.insertRow(rowCount);
		//for(var n=0;n<rowdataarray.length;n++)
		{
		 
			//Column 1  
			var cell1 = row.insertCell(0); 
			cell1.innerHTML = rowdataarray[1]; 
			
			//Column 2  
			var cell2 = row.insertCell(1); 
			cell2.innerHTML = rowdataarray[2]; 
			
			//Column 3  
			var cell3 = row.insertCell(2); 
			cell3.innerHTML = rowdataarray[3]; 
			
			//Column 4  
			var cell4 = row.insertCell(3); 
			cell4.innerHTML = rowdataarray[4]; 
			
			//Column 5  
			var cell5 = row.insertCell(4); 
			cell5.innerHTML = rowdataarray[5]; 
					
			
			//Column 6 
			var cell7 = row.insertCell(5); 
			cell7.innerHTML = "<a href='./static/"+foldername+"/"+rowdataarray[5]+"' target='_blank'> <i class='fa fa-eye' aria-hidden='true'></i></a>"; 
			
			
			//Column 4 
			var cell8 = row.insertCell(6); 
			//cell4.innerHTML = "<a href='delfile?id="+rowdataarray[0]+"&tblname="+tblname+"'> <i class='fa fa-trash' aria-hidden='true'></i></a>"; 
			cell8.innerHTML = "<a onclick='deletefile("+rowdataarray[0]+",\""+tblname+"\")'> <i class='fa fa-trash' aria-hidden='true'></i></a>"; 
			
		}
	}
	
	 
}

function deletefile(id,tblname)
{
	debugger;
	var fileid = id;
	var empid=document.getElementById('empid').value;
	if(tblname=="tblonboardingqual")
	{
        $.ajax({
            type: 'GET',
            url: '/delfile',
            data: {
			'empid':empid,
            'fileid': fileid,
            'tbl': tblname
			},
            dataType:"json",
            success: function(data) {
				console.log('file deleted in '+tblname);
				if(data!="")
				{
					document.getElementById('qualtablediv').style.display="block";
					document.getElementById("qualtable").innerHTML="";
					var table = document.getElementById("qualtable");					
					var header = table.createTHead();
					var row = header.insertRow(0);
					var cell = row.insertCell(0);
					cell.innerHTML = "<b>Qualification</b>";
					cell = row.insertCell(1);
					cell.innerHTML = "<b>Document</b>";
					cell = row.insertCell(2);
					cell.innerHTML = "<b>View</b>";
					cell = row.insertCell(3);
					cell.innerHTML = "<b>Delete</b>";
					data=data.replace("\"","");	
					data=data.substr(0,data.length-1);
					addRow('qualtable',data,'tblonboardingqual');
					alert('Deleted');
				}
				else{
					
					document.getElementById('qualtablediv').style.display="none";
					document.getElementById("qualtable").innerHTML="";
				}
            },
			 error: function(data) {
               
            }
        });
	}
	if(tblname=="tblonboardingcovidrep")
	{
        $.ajax({
            type: 'GET',
            url: '/delfile',
            data: {
			'empid':empid,
            'fileid': fileid,
            'tbl': tblname
			},
            dataType:"json",
            success: function(data) {
				console.log('file deleted in '+tblname);
				if(data!="")
				{
					document.getElementById('covidreptablediv').style.display="block";
					document.getElementById("covidreptable").innerHTML="";
					var table = document.getElementById("covidreptable");					
					var header = table.createTHead();
					var row = header.insertRow(0);
					var cell = row.insertCell(0);
					cell.innerHTML = "<b>Vaccination</b>";
					cell = row.insertCell(1);
					cell.innerHTML = "<b>Document</b>";
					cell = row.insertCell(2);
					cell.innerHTML = "<b>View</b>";
					cell = row.insertCell(3);
					cell.innerHTML = "<b>Delete</b>";
					data=data.replace("\"","");	
					data=data.substr(0,data.length-1);
					addRow('covidreptable',data,'tblonboardingcovidrep','CovidReports');
					alert('Deleted');
				}
				else{
					
					document.getElementById('covidreptablediv').style.display="none";
					document.getElementById("covidreptable").innerHTML="";
				}
            },
			 error: function(data) {
               
            }
        });
	}
	if(tblname=="tblonboardingidcard")
	{
        $.ajax({
            type: 'GET',
            url: '/delfile',
            data: {
			'empid':empid,
            'fileid': fileid,
            'tbl': tblname
			},
            dataType:"json",
            success: function(data) {
				console.log('file deleted in '+tblname);
				if(data!="")
				{
					document.getElementById('idcardtablediv').style.display="block";
					document.getElementById("idcardtable").innerHTML="";
					var table = document.getElementById("idcardtable");					
					var header = table.createTHead();
					var row = header.insertRow(0);
					var cell = row.insertCell(0);
					cell.innerHTML = "<b>Id Card</b>";
					cell = row.insertCell(1);
					cell.innerHTML = "<b>Document</b>";
					cell = row.insertCell(2);
					cell.innerHTML = "<b>View</b>";
					cell = row.insertCell(3);
					cell.innerHTML = "<b>Delete</b>";
					data=data.replace("\"","");	
					data=data.substr(0,data.length-1);
					addRow('idcardtable',data,'tblonboardingidcard','IdCards');
					alert('Deleted');
				}
				else
				{
					document.getElementById('idcardtablediv').style.display="none";
					document.getElementById("idcardtable").innerHTML="";
				}
            },
			 error: function(data) {
               
            }
        });
	}
	if(tblname=="tblonboardingscandoc")
	{
        $.ajax({
            type: 'GET',
            url: '/delfile',
            data: {
			'empid':empid,
            'fileid': fileid,
            'tbl': tblname
			},
            dataType:"json",
            success: function(data) {
				console.log('file deleted in '+tblname);
				if(data!="")
				{
					document.getElementById('scanlettertablediv').style.display="block";
					document.getElementById("scanlettertable").innerHTML="";
					var table = document.getElementById("scanlettertable");					
					var header = table.createTHead();
					var row = header.insertRow(0);
					var cell = row.insertCell(0);
					cell.innerHTML = "<b>Id Card</b>";
					cell = row.insertCell(1);
					cell.innerHTML = "<b>Document</b>";
					cell = row.insertCell(2);
					cell.innerHTML = "<b>Company Order</b>";
					cell = row.insertCell(3);
					cell.innerHTML = "<b>View</b>";
					cell = row.insertCell(4);
					cell.innerHTML = "<b>Delete</b>";
					data=data.replace("\"","");	
					data=data.substr(0,data.length-1);
					addRowScanDoc('scanlettertable',data,'tblonboardingscandoc','ScanDoc');
					alert('Deleted');
				}
				else{
					document.getElementById('scanlettertablediv').style.display="none";
					document.getElementById("scanlettertable").innerHTML="";
				}
            },
			 error: function(data) {
               
            }
        });
	}
	if(tblname=="tblonboardingexpcert")
	{
        $.ajax({
            type: 'GET',
            url: '/delfile',
            data: {
			'empid':empid,
            'fileid': fileid,
            'tbl': tblname
			},
            dataType:"json",
            success: function(data) {
				console.log('file deleted in '+tblname);
				if(data!="")
				{
					document.getElementById('expcerttablediv').style.display="block";
					document.getElementById("expcerttable").innerHTML="";
					var table = document.getElementById("expcerttable");					
					var header = table.createTHead();
					var row = header.insertRow(0);
					var cell = row.insertCell(0);
					cell.innerHTML = "<b>Company</b>";
					cell = row.insertCell(1);
					cell.innerHTML = "<b>From</b>";
					cell = row.insertCell(2);
					cell.innerHTML = "<b>To</b>";
					cell = row.insertCell(3);
					cell.innerHTML = "<b>Designation</b>";
					cell = row.insertCell(4);
					cell.innerHTML = "<b>Certificate</b>";
					cell = row.insertCell(5);
					cell.innerHTML = "<b>View</b>";
					cell = row.insertCell(6);
					cell.innerHTML = "<b>Delete</b>";
					data=data.replace("\"","");	
					data=data.substr(0,data.length-2);
					addRowExpCert('expcerttable',data,'tblonboardingexpcert','CertFile');
					alert('Deleted');
				}
				else{
					
					document.getElementById('expcerttablediv').style.display="none";
					document.getElementById("expcerttable").innerHTML="";
				}
            },
			 error: function(data) {
               
            }
        });
	}
}	

 
function removeRow(btnName) {  
debugger;
    try {  
        var table = document.getElementById('qualtable');  
        var rowCount = table.rows.length;  
        for (var i = 0; i < rowCount; i++) {  
            var row = table.rows[i];  
            var rowObj = row.cells[0].childNodes[0];  
            if (rowObj.name == btnName) {  
                table.deleteRow(i);  
                rowCount--;  
            }  
        }  
    } catch (e) {  
        alert(e);  
    }  
} 


$("#btn_hropsverifyonboarddata").click(function(){
debugger;
	//var empid=document.getElementById('empid').value;
	//window.location='verifyempstat1?empid='+empid;
	 var form_data = new FormData($('#upload-file')[0]);
        $.ajax({
            type: 'POST',
            url: '/verifyempstat1',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                console.log('Success!');
				alert('Data stored successfully');
            },
        });
});


$("#btn_verifyonboarddata").click(function(){
debugger;
	var empid=document.getElementById('empid').value;
	alert("Success");
	window.location='verifyempstat?empid='+empid;
	/*
        $.ajax({
            type: 'GET',
            url: '/verifyempstat',
            data: {
			'empid':empid
			},
            dataType:"json",
            success: function(data) {
				console.log('file deleted in '+tblname);
				window.location='verifyemp';
				
            },
			 error: function(data) {
               
            }
        });
		*/

});


$("#btn_updateveremp").click(function(){
debugger;
	var empid=document.getElementById('empid').value;
	window.location='updateverifyempstat?empid='+empid;
	/*
        $.ajax({
            type: 'GET',
            url: '/verifyempstat',
            data: {
			'empid':empid
			},
            dataType:"json",
            success: function(data) {
				console.log('file deleted in '+tblname);
				window.location='verifyemp';
				
            },
			 error: function(data) {
               
            }
        });
		*/

});


$("#btn_genmail").click(function(){
	debugger;
   var name = document.getElementById('ename').value;
   var email = document.getElementById('email').value;
   var phone = document.getElementById('phone').value;
        $.ajax({
            type: 'GET',
            url: '/genonboardmail',
            data: {
			'name':name,
			'email':email,
			'phone':phone
			},
            dataType:"json",
            success: function(data) {
				alert('Mail Sent');
				
            },
			 error: function(data) {
               
            }
        });
});

//Onboarding Save New Employee
$("#btn_saveonboarddata").click(function(){
	debugger;
	//Validation Script
	//Section -1
	if(document.getElementById('gender').value=="Select Gender")
	{
		alert('Please select gender');
		return false;
	}
	
	if(document.getElementById('edob').value=="")
	{
		alert('Please select DOB');
		return false;
	}
	
	var mail = document.getElementById('email').value;
	var mailpatt = /^[A-Za-z0-9$_?]+@[a-z0-9]+.[a-z]{2,3}$/;
	if(!mailpatt.test(mail))
	{
		alert("Please enter the email");
		return false;
	}		
	var mob = document.getElementById('phone').value;
	var mobpatt = /^[6|7|8|9]{1}[0-9]{9}$/
	if(!mobpatt.test(mob))
	{
		alert("Please enter the valid phone number");
		return false;
	}	
	/*
	var land = document.getElementById('landline').value;
	var landpatt = /^[0-9]{4}[0-9]{7}$/;
	if(!landpatt.test(land))
	{
		alert("Please enter the valid landline number");
		return false;
	}	
	*/
	if(document.getElementById('bgroup').value=="Select group")
	{
		alert("Please select Blood Group");
		return false;
	} 
	if(document.getElementById('ecat').value=="Select Category")
	{
		alert("Please select Employee Category");
		return false;
	} 
	var emcotname = document.getElementById('emeconname').value;	
	var emcotpatt = /^[A-Z a-z]{3,20}$/;
	if(!emcotpatt.test(emcotname))
	{
		alert("Please enter the contact name");
		return false;
	}
	var emcotnum = document.getElementById('emeconph').value;
	var emphpatt = /^[6|7|8|9]{1}[0-9]{9}$/;
	if(!emphpatt.test(emcotnum))
	{
		alert("Please enter the valid contact number");
		return false;
	}	
	var fathname = document.getElementById('fname').value;
	var fatpatt = /^[A-Z a-z]{3,20}$/;
	if(!fatpatt.test(fathname))
	{
		alert("Please enter the father name");
		return false;
	}
	var motname = document.getElementById('mname').value;
	var motpatt = /^[A-Z a-z]{3,20}$/;
	if(!motpatt.test(motname))
	{
		alert("Please enter the mother name");
		return false;
	}
	var add = document.getElementById('paddr').value;
	var addpatt = /^[A-Z a-z 0-9 ]{3,50}$/;
	if(!addpatt.test(add))
	{
		alert("Please enter the address");
		return false;
	}
	/*
	var temadd = document.getElementById('taddr').value;
	var temaddpatt = /^[A-Z a-z 0-9 ]{3,50}$/;
	if(!temaddpatt.test(temadd))
	{
		alert("Please enter the temporary address");
		return false;
	}
	*/
	if(document.getElementById('mstatus').value == "Select Status")
	{
		alert("Please select Status");
		return false;
	} 
	if(document.getElementById('mstatus').value == "Married")
	{
		if(document.getElementById('sponame').value == "")
		
		alert("Please select Spouse Name");
		return false;
	} 
	
	if(document.getElementById('imgfile').files.length==0)
	{
		alert("Please select image");
		return false;
	}
	
	//End of Section 1

	//Start of Section 2
	if(document.getElementById('qual').value == "0")
	{
		alert("Please select Qualification details");
		return false;
	}
	if(document.getElementById('govtidcard').value == "0")
	{
		alert("Please selectid proof");
		return false;
	}
	/*
	if(document.getElementById('scanletter').value == "0")
	{
		alert("Please select Letter");
		return false;
	}
	
	if(document.getElementById('comporder').value=="0")
	{
		alert("Please select the Company Order");
		return false;
	}
	*/
	if(document.getElementById('cvaacine').value=="")
	{
		alert("Please add the Covid Vaccination details");
		return false;
	}

	//End of Section 2

	//Start Section 3
	var doj = document.getElementById('doj').value;
	if(doj=='')
	{ 
		alert("Please enter date of joining");
		return false;
	}
	var idate = document.getElementById('idate').value;
	if(idate=='')
	{ 
		alert("Please enter date of interview");
		return false;
	}
	/*
	var bg = document.getElementById('bgv').value;
	var bgpatt = /^[A-Z a-z 0-9 ]{3,50}$/;
	if(!bgpatt.test(bg))
	{ 
		alert("Please fill the B.G Verified");
		return false;
	}
	
	var reaof = document.getElementById('reason').value;
	var resonpat = /^[A-Z a-z 0-9 ]{3,50}$/;
	if(!resonpat.test(reaof))
	{
		alert("Please fill the Reason of Exit");
		return false;
	}*/
	//End Section 3
	//Start Section 4
	if(document.getElementById('walkinsource').value=="No Source")
	{
		alert("Please fill the Source");
		return false;
	}
	if(document.getElementById('exp').value=="0")
	{
		alert("Please Select the Experience details");
		return false;
	}
	if(document.getElementById('depts').value=="-- Select Department --")
	{
		alert("Please Select the Department");
		return false;
	}
	if(document.getElementById('process').value=="0")
	{
		alert("Please Select the Process");
		return false;
	}
	if(document.getElementById('position').value=="0")
	{
		alert("Please Select the Positon");
		return false;
	}
	if(document.getElementById('mgrnm').value=="")
	{
		alert("Please Select the Manager name");
		return false;
	}
	if(document.getElementById('amgrnm').value=="")
	{
		alert("Please Select the Asst Manager name");
		return false;
	}	
	//End Section 4
	//Start Section 5
	/*
	var ctc = document.getElementById('ctc').value;
	var ctcpatt = /^[0-9]{10}$/;
	if(!ctcpatt.test(ctc))
	{
		alert("Please enter the CTC");
		return false;
	}
	if(document.getElementById('bname').value=="0")
	{
		alert("Please Select the Bank name");
		return false;
	}
	var ifc = document.getElementById('ifsc').value;
	var ifscpatt = "/^[A-Za-Z0-9]{3,20}$/";
	if(!ifscpatt.test(ifc))
	{
		alert("Please enter the ifsc code");
		return false;
	}
	var accname = document.getElementById('accname').value;
	var accnmepatt = /^[A-Za-z]{3,20}$/;
	if(!accnmepatt.test(accname))
	{
		alert("Please enter the Name as per Bank");
		return false;
	}
	var brchnme = document.getElementById('branchname').value;
	var brchnmepatt = /^[A-Z a-z]{3,20}$/;
	if(!brchnmepatt.test(brchnme))
	{
		alert("Please enter the BranchName");
		return false;
	}
	var partwge = document.getElementById('partwagehr').value;
	var partpatt = /^[A-Z a-z]{3,20}$/;
	if(!partpatt.test(partwge))
	{
		alert("Please enter the ParTime wages/hour");
		return false;
	}
	var bankacc = document.getElementById('baccnum').value;
	var bankpatt = /^[0-9]{3,20}$/;
	if(!bankpatt.test(bankacc))
	{
		alert("Please enter the Bank account number");
		return false;
	}	
	var insrnce = document.getElementById('minsnum').value;
	var insrncepatt = /^[A-Z a-z]{3,20}$/;
	if(!insrncepatt.test(insrnce))
	{
		alert("Please enter the Medical Insurance Number");
		return false;
	}	
	var mednsrnceamt = document.getElementById('minsamt').value;
	var mednsrnceamtpatt = /^[0-9]{3,20}$/;
	if(!mednsrnceamtpatt.test(mednsrnceamt))
	{
		alert("Please enter the Medical Insurance Amount");
		return false;
	}
	var oldpf = document.getElementById('opf').value;
	var oldpfpatt = /^[0-9]{3,20}$/;
	if(!oldpfpatt.test(oldpf))
	{
		alert("Please enter the Old pf Number");
		return false;
	}
	var oldesi = document.getElementById('oesi').value;
	var oldesipatt = /^[0-9]{3,20}$/;
	if(!oldesipatt.test(oldesi))
	{
		alert("Please enter the Old ESI Number");
		return false;
	}
	var uan = document.getElementById('uan').value;
	var uanpatt = /^[0-9]{3,20}$/;
	if(!uanpatt.test(uan))
	{
		alert("Please enter the UAN Number");
		return false;
	}
	var esin = document.getElementById('esinum').value;
	var esinpatt = /^[0-9]{3,20}$/;
	if(!esinpatt.test(esin))
	{
		alert("Please enter the ESI Number");
		return false;
	}	
	if(document.getElementById('edstatus').value=="0")
	{
		alert("Please Select the Document Status");
		return false;
	}*/
	
	//End Section 5
	//End
   var form_data = new FormData($('#upload-file')[0]);
        $.ajax({
            type: 'POST',
            url: '/savenewemp',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                console.log('Success!');
				alert('Data stored successfully');
            },
        });
	
});

//Onboarding Save New Employee
$("#btn_resetonboarddata").click(function(){
	debugger;
	$('#upload-file').trigger("reset");
	
});

//Onboarding Save New Employee
$("#btn_saveconboarddata").click(function(){
	debugger;
	
	//Validation Script
	//Section -1
	if(document.getElementById('gender').value=="Select Gender")
	{
		alert('Please select gender');
		return false;
	}

	if(document.getElementById('edob').value=="")
	{
		alert('Please select DOB');
		return false;
	}
	
	var mail = document.getElementById('email').value;
	var mailpatt = /^[A-Za-z0-9$_?]+@[a-z0-9]+.[a-z]{2,3}$/;
	if(!mailpatt.test(mail))
	{
		alert("Please enter the email");
		return false;
	}		
	var mob = document.getElementById('phone').value;
	var mobpatt = /^[6|7|8|9]{1}[0-9]{9}$/
	if(!mobpatt.test(mob))
	{
		alert("Please enter the valid phone number");
		return false;
	}	
	/*
	var land = document.getElementById('landline').value;
	var landpatt = /^[0-9]{4}[0-9]{7}$/;
	if(!landpatt.test(land))
	{
		alert("Please enter the valid landline number");
		return false;
	}	
	*/
	if(document.getElementById('bgroup').value=="Select group")
	{
		alert("Please select Blood Group");
		return false;
	} 
	var emcotname = document.getElementById('emeconname').value;	
	var emcotpatt = /^[A-Z a-z]{3,20}$/;
	if(!emcotpatt.test(emcotname))
	{
		alert("Please enter the contact name");
		return false;
	}
	var emcotnum = document.getElementById('emeconph').value;
	var emphpatt = /^[6|7|8|9]{1}[0-9]{9}$/;
	if(!emphpatt.test(emcotnum))
	{
		alert("Please enter the valid contact number");
		return false;
	}	
	var fathname = document.getElementById('fname').value;
	var fatpatt = /^[A-Z a-z]{3,20}$/;
	if(!fatpatt.test(fathname))
	{
		alert("Please enter the father name");
		return false;
	}
	var motname = document.getElementById('mname').value;
	var motpatt = /^[A-Z a-z]{3,20}$/;
	if(!motpatt.test(motname))
	{
		alert("Please enter the mother name");
		return false;
	}
	var add = document.getElementById('paddr').value;
	var addpatt = /^[A-Z a-z 0-9 ]{3,50}$/;
	if(!addpatt.test(add))
	{
		alert("Please enter the address");
		return false;
	}
	/*
	var temadd = document.getElementById('taddr').value;
	var temaddpatt = /^[A-Z a-z 0-9 ]{3,50}$/;
	if(!temaddpatt.test(temadd))
	{
		alert("Please enter the temporary address");
		return false;
	}
	*/
	if(document.getElementById('mstatus').value == "Select Status")
	{
		alert("Please select Status");
		return false;
	} 
	if(document.getElementById('mstatus').value == "Married")
	{
		if(document.getElementById('sponame').value == "")
		
		alert("Please select Spouse Name");
		return false;
	} 
	if(document.getElementById('imgfile').files.length==0)
	{
		alert("Please select image");
		return false;
	}
	
	//End of Section 1

	//Start of Section 2
	if(document.getElementById('qual').value == "0")
	{
		alert("Please select Qualification details");
		return false;
	}
	if(document.getElementById('govtidcard').value == "0")
	{
		alert("Please selectid proof");
		return false;
	}
	/*
	if(document.getElementById('scanletter').value == "0")
	{
		alert("Please select Letter");
		return false;
	}
	
	if(document.getElementById('comporder').value=="0")
	{
		alert("Please select the Company Order");
		return false;
	}
	*/
	if(document.getElementById('cvaacine').value=="")
	{
		alert("Please add the Covid Vaccination details");
		return false;
	}

	//End of Section 2

	//Start Section 3
	
	if(document.getElementById('exp').value=="0")
	{
		alert("Please Select the Experience");
		return false;
	}
	
	//End of Section 3
	
	//End
	
   var form_data = new FormData($('#upload-file')[0]);
        $.ajax({
            type: 'POST',
            url: '/savenewemp1',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                console.log('Success!');
				alert('Data stored successfully');
            },
        });
	
	
});



//Soure of Walkin Save New 
$("#btn_savesow").click(function(){
	debugger;
	var btnnm=document.getElementById('btn_savesow').value;
	var sow=document.getElementById('sow').value;
	var sowid=document.getElementById('sowid').value;
	var stype='';
	if(btnnm=="Save data")
	{
		stype='New';
	}
	else{
		stype='Update';
	}
		
    $.ajax({
            type: 'GET',
            url: '/addsow',
            data: {
			'sow':sow,
			'sowid':sowid,
			'type':stype
			},
            dataType:"json",
            success: function(data) {
				if(data!="")
				{
					document.getElementById("walkintable").innerHTML="";
					var table = document.getElementById("walkintable");					
					var header = table.createTHead();
					var row = header.insertRow(0);
					var cell = row.insertCell(0);
					cell.innerHTML = "<b>Source</b>";
					cell = row.insertCell(1);
					cell.innerHTML = "<b>Edit</b>";
					cell = row.insertCell(2);
					cell.innerHTML = "<b>Delete</b>";
					data=data.replace("\"","");	
					data=data.substr(0,data.length-1);
					addSrcRow('walkintable',data);
					alert('Row Added');
				}
				
            },
			 error: function(data) {
               
            }
        });
	
	
});


function addSrcRow(tableID,data) {  
	debugger;
	
	var table = document.getElementById(tableID);  
	var dataarray = data.split("#");
	for(var m=0;m<dataarray.length;m++)
	{
		var rowdata=dataarray[m];
		var rowdataarray = rowdata.split(",");
		 
		var rowCount = table.rows.length;  
		var row = table.insertRow(rowCount);
		//for(var n=0;n<rowdataarray.length;n++)
		{
		 
			//Column 1  
			var cell1 = row.insertCell(0); 
			cell1.innerHTML = rowdataarray[1]; 
			
			//Column 2  
			var cell2 = row.insertCell(1); 
			cell2.innerHTML = "<a onclick='editsrc("+rowdataarray[0]+",\""+rowdataarray[1]+"\")'><i class='fa fa-edit' aria-hidden='true'></i></a>"; 
			
			//Column 3  
			var cell3 = row.insertCell(2); 
			cell3.innerHTML = "<a href='deletesrc?id="+rowdataarray[0]+"'> <i class='fa fa-trash' aria-hidden='true'></i></a>"; 
			
			
		}
	}
	
	 
}

function editsrc(id,data)
{
	document.getElementById('sow').value=data.trim();
	document.getElementById('sowid').value=id;
	document.getElementById('btn_savesow').value="Update Data";
}




$('input:radio').click(function() {
	debugger;
	var ctc=document.getElementById('ctc').value;
    if ($(this).val() === '1') {
		var ctc=document.getElementById('ctc').value;
		ctc=parseFloat(ctc);		
		var bsal=document.getElementById('bsal').value;
		bsal=parseFloat(bsal);
		var emplyrpfper=0.13;
		var emplyresicper=0.0325;
		var emppfper=0.12;
		var empesicper=0.0075;
		var pt=200;
		var emplyresic=emplyresicper*ctc;
		var emplyrpf=emplyrpfper*bsal;
		var gsal=ctc-(emplyresic+emplyrpf);
		var empesic=empesicper*gsal;
		var emppf=emppfper*bsal;
		if(gsal<15000)
		{
			pt=0;
		}
		var netsal=gsal-(empesic+emppf+pt);
		
		document.getElementById('bsal').value=bsal.toFixed(2);
		document.getElementById('gsal').value=gsal.toFixed(2);
		document.getElementById('nsal').value=netsal.toFixed(2);
		document.getElementById('proftax').value=pt;
		document.getElementById('emplyrpf').value=emplyrpf.toFixed(2);
		document.getElementById('emppf').value=emppf.toFixed(2);
		document.getElementById('emplyresic').value=emplyresic.toFixed(2);
		document.getElementById('empesic').value=empesic.toFixed(2);


		/*
		if(ctc=="19000"){
		document.getElementById('emplyrpf').value="845";
		document.getElementById('emppf').value="780";
		
		document.getElementById('gsal').value="17537.5";
		document.getElementById('nsal').value="16425.9";
		}
		if(ctc=="13500"){
		document.getElementById('emplyrpf').value="845";
		document.getElementById('emppf').value="780";
		document.getElementById('gsal').value="12216.2";
		document.getElementById('nsal').value="11344.6";
		}
		if(ctc=="50000"){
		document.getElementById('emplyrpf').value="1950";
		document.getElementById('emppf').value="1800";
		document.getElementById('gsal').value="48050";
		document.getElementById('nsal').value="44050";
		}
		*/
    } else if ($(this).val() === '2') {
		
		document.getElementById('emplyrpf').value="0";
		document.getElementById('emppf').value="0";
		var ctc=document.getElementById('ctc').value;
		ctc=parseFloat(ctc);
		var bsal=document.getElementById('bsal').value;
		bsal=parseFloat(bsal);
		
		var gsal=parseFloat(document.getElementById('gsal').value);
		var netsal=parseFloat(document.getElementById('nsal').value);
		var emplyrpfper=0.13;
		var emplyresicper=0.0325;
		var emppfper=0.12;
		var empesicper=0.0075;
		var pt=200;
		var emplyrpf=emplyrpfper*bsal;
		var gsal=gsal+emplyrpf;
		var emppf=emppfper*bsal;
		var empesic=empesicper*gsal;
		if(gsal<15000)
		{
			pt=0;
		}
		var netsal=(gsal)-(empesic+pt);
		
		document.getElementById('gsal').value=gsal.toFixed(2);
		document.getElementById('nsal').value=netsal.toFixed(2);
		document.getElementById('proftax').value=pt;
		/*
		document.getElementById('emplyrpf').value="0";
		document.getElementById('emppf').value="0";
		if(ctc=="19000"){
		 document.getElementById('gsal').value="18382.5";
		 document.getElementById('nsal').value="18044.6";
		}
		if(ctc=="13500"){
		 document.getElementById('gsal').value="13061.2";
		 document.getElementById('nsal').value="12963.2.6";
		}
		if(ctc=="50000"){
		 document.getElementById('gsal').value="50000";
		 document.getElementById('nsal').value="47800";
		}
		*/
    } 
	 else if ($(this).val() === '3') {		 
		 
		if(ctc=="50000"){
		document.getElementById('emplyresic').value="0";
		document.getElementById('empesic').value="0";
		}
		else{
			
			var ctc=document.getElementById('ctc').value;
			ctc=parseFloat(ctc);		
			var bsal=document.getElementById('bsal').value;
			bsal=parseFloat(bsal);
			var emplyrpfper=0.13;
			var emplyresicper=0.0325;
			var emppfper=0.12;
			var empesicper=0.0075;
			var pt=200;
			var emplyresic=emplyresicper*ctc;
			var emplyrpf=emplyrpfper*bsal;
			var gsal=ctc-(emplyresic+emplyrpf);
			var empesic=empesicper*gsal;
			var emppf=emppfper*bsal;
			if(gsal<15000)
			{
				pt=0;
			}
			var netsal=gsal-(empesic+emppf+pt);
			
			document.getElementById('bsal').value=bsal.toFixed(2);
			document.getElementById('gsal').value=gsal.toFixed(2);
			document.getElementById('nsal').value=netsal.toFixed(2);
			document.getElementById('proftax').value=pt;
			document.getElementById('emplyresic').value=emplyresic.toFixed(2);
			document.getElementById('empesic').value=empesic.toFixed(2);

		}
    } else if ($(this).val() === '4') {
		document.getElementById('emplyresic').value="0";
		document.getElementById('empesic').value="0";
		var ctc=document.getElementById('ctc').value;
		ctc=parseFloat(ctc);
		
		var bsal=document.getElementById('bsal').value;
		bsal=parseFloat(bsal);
		var gsal=parseFloat(document.getElementById('gsal').value);
		var netsal=parseFloat(document.getElementById('nsal').value);
		var emplyrpfper=0.13;
		var emplyresicper=0.0325;
		var emppfper=0.12;
		var empesicper=0.0075;
		var pt=200;
		var emplyresic=emplyresicper*ctc;
		var emplyrpf=emplyrpfper*bsal;
		var gsal=ctc-(emplyrpf);
		var empesic=empesicper*gsal;
		var emppf=emppfper*bsal;
		
		if(gsal<15000)
		{
			pt=0;
		}
		var netsal=gsal-(emppf+pt);
		
		document.getElementById('bsal').value=bsal.toFixed(2);
			document.getElementById('gsal').value=gsal.toFixed(2);
			document.getElementById('nsal').value=netsal.toFixed(2);
			document.getElementById('proftax').value=pt;
			document.getElementById('emplyrpf').value=emplyrpf.toFixed(2);
			document.getElementById('emppf').value=emppf.toFixed(2);
    } 
  });



  //Save New Appraisal
$("#saveappraisal").click(function(){
	debugger;
   var cbs = document.getElementById('cbs').value;
   var cgs = document.getElementById('cgs').value;
   var cctc = document.getElementById('cctc').value;
   var cns = document.getElementById('cns').value;
   var mon = document.getElementById('mon').value;
   var year = document.getElementById('year').value;
   var comment = document.getElementById('comment').value;
   var empcode = document.getElementById('empcode').value;
        $.ajax({
            type: 'GET',
            url: '/saveappraisal',
            data: {
			'cbs':cbs,
			'cgs':cgs,
			'cctc':cctc,
			'cns':cns,
			'mon':mon,
			'year':year,
			'comment':comment,
			'empcode':empcode
			},
            dataType:"json",
            success: function(data) {
				alert('Data Saved');
				window.open('addappraisal?empcode='+empcode)
				
            },
			 error: function(data) {
               
            }
        });
});
//Add Process - Mgr Amgr
$("#btn_saveproc").click(function(){
	debugger;
	var btnnm=document.getElementById('btn_saveproc').value;
	var proc=document.getElementById('proc').value;
	var procid=document.getElementById('procid').value;
	var mgr=document.getElementById('mgr').value;
	var amgr=document.getElementById('amgr').value;
	var teval="";
	var icval="";
	if(document.getElementById('te1').checked)
	{
		teval="Yes";
	}
	if(document.getElementById('te2').checked)
	{
		teval="No";
	}

	if(document.getElementById('ic1').checked)
	{
		icval="Yes";
	}
	if(document.getElementById('ic2').checked)
	{
		icval="No";
	}

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
            url: '/addproc',
            data: {
			'proc':proc,
			'procid':procid,
			'mgr':mgr,
			'amgr':amgr,
			'teval':teval,
			'icval':icval,
			'type':stype
			},
            dataType:"json",
            success: function(data) {
				if(data!="")
				{
					document.getElementById("proctable").innerHTML="";
					var table = document.getElementById("proctable");					
					var header = table.createTHead();
					
					header.className="bg-darkblue text-white border-darkblue";
					var row = header.insertRow(0);
					var cell = row.insertCell(0);
					cell.innerHTML = "<b>Process</b>";
					cell = row.insertCell(1);
					cell.innerHTML = "<b>Manager Name</b>";
					cell = row.insertCell(2);
					cell.innerHTML = "<b>Asst. Manager Name</b>";
					var cell = row.insertCell(3);
					cell.innerHTML = "<b>Time Excluded</b>";
					var cell = row.insertCell(4);
					cell.innerHTML = "<b>Is Common</b>";
					cell = row.insertCell(5);
					cell.innerHTML = "<b>Edit</b>";
					cell = row.insertCell(6);
					cell.innerHTML = "<b>Delete</b>";
					data=data.replace("\"","");	
					data=data.substr(0,data.length-1);
					addProcRow('proctable',data);
					alert('Row Added');
				}
				
            },
			 error: function(data) {
               
            }
        });
	
	
});



function addProcRow(tableID,data) {  
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
		//var row = table.insertRow(rowCount);
		//for(var n=0;n<rowdataarray.length;n++)
		{
		 
			//Column 1  
			var cell1 = row.insertCell(0); 
			cell1.innerHTML = rowdataarray[1]; 
			//Column 1  
			var cell2= row.insertCell(1); 
			cell2.innerHTML = rowdataarray[2]; 
			//Column 1  
			var cell3 = row.insertCell(2); 
			cell3.innerHTML = rowdataarray[3]; 
			//Column 1  
			var cell4 = row.insertCell(3); 
			cell4.innerHTML = rowdataarray[4]; 
			//Column 1  
			var cell5 = row.insertCell(4); 
			cell5.innerHTML = rowdataarray[5]; 
			
			//Column 2  
			var cell6 = row.insertCell(5); 
			cell6.innerHTML = "<a onclick='editproc("+rowdataarray[0]+",\""+rowdataarray[1]+"\")'><i class='fa fa-edit' aria-hidden='true'></i></a>"; 
			
			//Column 3  
			var cell7 = row.insertCell(6); 
			cell7.innerHTML = "<a href='deleteproc?id="+rowdataarray[0]+"'> <i class='fa fa-trash' aria-hidden='true'></i></a>"; 
			
			
		}
	}	 
}

function editproc(id,data,mgr,amgr,te,ic)
{
	debugger;
	document.getElementById('proc').value=data.trim();
	document.getElementById('procid').value=id;
	document.getElementById('mgr').value=mgr.trim();
	document.getElementById('amgr').value=amgr.trim();
	if(te=="Yes")
	{
		document.getElementById('te1').checked=true;
	}
	if(te=="No")
	{
		document.getElementById('te2').checked=true;
	}
	if(ic=="Yes")
	{
		document.getElementById('ic1').checked=true;
	}
	if(ic=="No")
	{
		document.getElementById('ic2').checked=true;
	}
	document.getElementById('btn_saveproc').value="Update Data";
}

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
					header.className="bg-darkblue text-white border-darkblue";
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
	var body = table.createTBody();
	var dataarray = data.split("#");
	for(var m=0;m<dataarray.length;m++)
	{
		var rowdata=dataarray[m];
		var rowdataarray = rowdata.split(",");
		 
		var rowCount = 0;//table.rows.length;  
		//var row = table.insertRow(rowCount);
		var row = body.insertRow(rowCount);
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


//Add New Role
$("#btn_addnewrole").click(function(){
	debugger;
	var rolename=document.getElementById('rolename').value;
		
    $.ajax({
            type: 'GET',
            url: '/addnewrole',
            data: {
			'rolename':rolename
			},
            dataType:"json",
            success: function(data) {
				alert('Role added successfully');	
				window.location='rolecreation';			
            },
			 error: function(data) {
               
            }
        });
});

$("#btn_clearnewrole").click(function(){
	window.location='rolecreation';
});


//Add New Language
$("#btn_addnewlang").click(function(){
	debugger;
	var lang=document.getElementById('lang').value;
		
    $.ajax({
            type: 'GET',
            url: '/addnewlang',
            data: {
			'lang':lang
			},
            dataType:"json",
            success: function(data) {
				alert('Language added successfully');	
				window.location='languages';			
            },
			 error: function(data) {
               
            }
        });
});

$("#btn_clearnewlang").click(function(){
	window.location='languages';
});

//Change Password
$("#btn_addnewchngpswd").click(function(){
	debugger;
	var ru_cpswd=document.getElementById('ru_cpswd').value;
	var ru_email=document.getElementById('ru_email').value;
		
    $.ajax({
            type: 'GET',
            url: '/changepswd',
            data: {
			'ru_email':ru_email,
			'ru_cpswd':ru_cpswd
			},
            dataType:"json",
            success: function(data) {
				alert('Passsword Changed successfully');	
				window.location='chngpswd';			
            },
			 error: function(data) {
               
            }
        });
});

$("#btn_clearnewchngpswd").click(function(){
	window.location='chngpswd';
});


//Add New Bank
$("#btn_addnewbank").click(function(){
	debugger;
	var bank=document.getElementById('bank').value;
		
    $.ajax({
            type: 'GET',
            url: '/addnewbank',
            data: {
			'bank':bank
			},
            dataType:"json",
            success: function(data) {
				alert('Bank Name added successfully');	
				window.location='banks';			
            },
			 error: function(data) {
               
            }
        });
});

$("#btn_clearnewbank").click(function(){
	window.location='banks';
});


//Add New Holiday
$("#btn_addnewhdate").click(function(){
	debugger;
	var hname=document.getElementById('hname').value;
	var dated=document.getElementById('dated').value;
		
    $.ajax({
            type: 'GET',
            url: '/addnewhdate',
            data: {
			'hname':hname,
			'dated':dated
			},
            dataType:"json",
            success: function(data) {
				alert('Leave added successfully');	
				window.location='holidaycal';			
            },
			 error: function(data) {
               
            }
        });
});

$("#btn_clearnewhdate").click(function(){
	window.location='holidaycal';
});


//Add New IP
$("#btn_addnewip").click(function(){
	debugger;
	var ipaddr=document.getElementById('ipaddr').value;
		
    $.ajax({
            type: 'GET',
            url: '/addnewip',
            data: {
			'ipaddr':ipaddr
			},
            dataType:"json",
            success: function(data) {
				alert('Ip Address added successfully');	
				window.location='ipaddrs';			
            },
			 error: function(data) {
               
            }
        });
});

$("#btn_clearnewip").click(function(){
	window.location='ipaddrs';
});

//Add New Weblogins
$("#btn_addnewweblogin").click(function(){
	debugger;
	var ru_email=document.getElementById('ru_email').value;
	var ru_pswd=document.getElementById('ru_pswd').value;
		
    $.ajax({
            type: 'GET',
            url: '/addnewweblogin',
            data: {
			'ru_email':ru_email,
			'ru_pswd':ru_pswd
			},
            dataType:"json",
            success: function(data) {
				alert('Web login added successfully');	
				window.location='weblogins';			
            },
			 error: function(data) {
               
            }
        });
});

$("#btn_clearnewweblogin").click(function(){
	window.location='weblogins';
});



//Add New Subject
$("#btn_addnewsub").click(function(){
	debugger;
	var sub=document.getElementById('sub').value;
	var stype=document.getElementById('stype').value;
	var course=document.getElementById('course').value;
	var sem=document.getElementById('sem').value;
	var credit=document.getElementById('credit').value;
	var subcode=document.getElementById('subcode').value;
	var seats=document.getElementById('seats').value;
	var exclusion=document.getElementById('exclusion').value;
		
    $.ajax({
            type: 'GET',
            url: '/addnewsub',
            data: {
			'sub':sub,
			'stype':stype,
			'course':course,
			'sem':sem,
			'credit':credit,
			'subcode':subcode,
			'seats':seats,
			'exclusion':exclusion

			},
            dataType:"json",
            success: function(data) {
				alert('Subject added successfully');	
				window.location='asubjects';			
            },
			 error: function(data) {
               
            }
        });
});

$("#btn_clearnewsub").click(function(){
	window.location='asubjects';
});



//Add New Round
$("#btn_addnewround").click(function(){
	debugger;
	var sdate=document.getElementById('sdate').value;
	var edate=document.getElementById('edate').value;
	var round=document.getElementById('round').value;
		
    $.ajax({
            type: 'GET',
            url: '/addnewround',
            data: {
			'sdate':sdate,
			'edate':edate,			
			'round':round

			},
            dataType:"json",
            success: function(data) {
				alert('Round Created Successfully');	
				window.location='aaddrounds';			
            },
			 error: function(data) {
               
            }
        });
});

$("#btn_clearnewround").click(function(){
	window.location='aaddrounds';
});



//Add New Blog
$("#btn_addnewblog").click(function(){
	debugger;
	var sub=document.getElementById('sub').value;
	var course=document.getElementById('course').value;
	var sem=document.getElementById('sem').value;
	var usn=document.getElementById('usn').value;
	var scode=document.getElementById('scode').value;
	var credits=document.getElementById('credits').value;
		
    $.ajax({
            type: 'GET',
            url: '/addnewblog',
            data: {
			'sub':sub,
			'course':course,
			'sem':sem,
			'usn':usn,
			'scode':scode,
			'credits':credits

			},
            dataType:"json",
            success: function(data) {
				alert('Backlog added successfully');	
				window.location='abacklogs';			
            },
			 error: function(data) {
               
            }
        });
});

$("#btn_clearnewblog").click(function(){
	window.location='abacklogs';
});


//Add New Mentors
$("#btn_addnewmentor").click(function(){
	debugger;
	var mname=document.getElementById('mname').value;
	var course=document.getElementById('course').value;
	var sem=document.getElementById('sem').value;
	var uname=document.getElementById('uname').value;
	var pswd=document.getElementById('pswd').value;
	var email=document.getElementById('email').value;
		
    $.ajax({
            type: 'GET',
            url: '/addnewmentor',
            data: {
			'mname':mname,
			'course':course,
			'uname':uname,
			'sem':sem,
			'pswd':pswd,
			'email':email

			},
            dataType:"json",
            success: function(data) {
				alert('Mentor added successfully');	
				window.location='hmentors';			
            },
			 error: function(data) {
               
            }
        });
});

$("#btn_clearnewmentor").click(function(){
	window.location='hmentors';
});


//Add New Mentors to Students
$("#btn_addstumentor").click(function(){
	debugger;
	var mname=document.getElementById('mname').value;
	var usn=document.getElementById('usn').value;
    $.ajax({
            type: 'GET',
            url: '/addstumentor',
            data: {
			'mname':mname,
			'usn':usn

			},
            dataType:"json",
            success: function(data) {
				alert('Student has been allocated');	
				window.location='hallocstudents';			
            },
			 error: function(data) {
               
            }
        });
});

$("#btn_clearstumentor").click(function(){
	window.location='hallocstudents';
});


//Add New Pay Type
$("#btn_addnewpaytype").click(function(){
	debugger;
	var paytype=document.getElementById('paytype').value;
	var paycode=document.getElementById('paycode').value;
	var color=document.getElementById('color').value;
		
    $.ajax({
            type: 'GET',
            url: '/addnewpaytype',
            data: {
			'paytype':paytype,
			'paycode':paycode,
			'color':color
			},
            dataType:"json",
            success: function(data) {
				alert('Pay Type added successfully');	
				window.location='paytype';			
            },
			 error: function(data) {
               
            }
        });
});

$("#btn_clearpaytype").click(function(){
	window.location='paytype';
});

//Shift Type Management
$("#btn_addnewshift").click(function(){
	debugger;
	var sname=document.getElementById('sname').value;
	var intime=document.getElementById('intime').value;
	var outtime=document.getElementById('outtime').value;
	var hdhour=document.getElementById('hdhour').value;
	var fdhour=document.getElementById('fdhour').value;
	var nshift="";
	if (document.getElementById('nshift').checked==true)
	{
		nshift="Yes";
	}
	else{
		nshift="No";
	}
		
    $.ajax({
            type: 'GET',
            url: '/addnewshift',
            data: {
			'sname':sname,
			'intime':intime,
			'outtime':outtime,
			'hdhour':hdhour,
			'fdhour':fdhour,
			'nshift':nshift
			},
            dataType:"json",
            success: function(data) {
				alert('Shift Timing added successfully');	
				window.location='shifttiming';			
            },
			 error: function(data) {
               
            }
        });
});

$("#btn_clearnewshift").click(function(){
	window.location='shifttiming';
});

//Add New Department
$("#btn_addnewdept").click(function(){
	debugger;
	var dept=document.getElementById('dept').value;
		
    $.ajax({
            type: 'GET',
            url: '/addnewdept',
            data: {
			'dept':dept
			},
            dataType:"json",
            success: function(data) {
				alert('Department added successfully');	
				window.location='departments';			
            },
			 error: function(data) {
               
            }
        });
});

$("#btn_clearnewdept").click(function(){
	window.location='departments';
});


//Add New Position
$("#btn_addnewposition").click(function(){
	debugger;
	var position=document.getElementById('position').value;
		
    $.ajax({
            type: 'GET',
            url: '/addnewposition',
            data: {
			'position':position
			},
            dataType:"json",
            success: function(data) {
				alert('Position added successfully');	
				window.location='positions';			
            },
			 error: function(data) {
               
            }
        });
});

$("#btn_clearnewposition").click(function(){
	window.location='positions';
});



//Add New id proof
$("#btn_addnewidproof").click(function(){
	debugger;
	var idproof=document.getElementById('idproof').value;
		
    $.ajax({
            type: 'GET',
            url: '/addnewidproof',
            data: {
			'idproof':idproof
			},
            dataType:"json",
            success: function(data) {
				alert('Id proof added successfully');	
				window.location='idproofs';			
            },
			 error: function(data) {
               
            }
        });
});

//Fetch manager on process
function fetchuserdata(){
	debugger;
	var empid=document.getElementById('ru_empid').value;
		
    $.ajax({
            type: 'GET',
            url: '/fetchmgrpersonaldata',
            data: {
			'empid':empid
			},
            dataType:"json",
            success: function(data) {
				dataval=data.split(',');
				document.getElementById('ru_uname').value=dataval[0];
				document.getElementById('ru_email').value=dataval[1];
            },
			 error: function(data) {
               
            }
        });
	}

//Fetch manager on process
function fetchuserdata1(){
	debugger;
	var empid=document.getElementById('ru_empid').value;
		
    $.ajax({
            type: 'GET',
            url: '/fetchroledata',
            data: {
			'empid':empid
			},
            dataType:"json",
            success: function(data) {
				dataval=data.split(',');
				document.getElementById('ru_uname').value=dataval[0];
				document.getElementById('ru_email').value=dataval[1];
				document.getElementById('ru_pswd').value=dataval[2];
            },
			 error: function(data) {
               
            }
        });
	}


//Fetch manager on process
$("#proc").change(function(){
	debugger;
	var proc=document.getElementById('proc').value;
		
    $.ajax({
            type: 'GET',
            url: '/fetchprocmgr',
            data: {
			'proc':proc
			},
            dataType:"json",
            success: function(data) {
				document.getElementById('mgr').value=data;
            },
			 error: function(data) {
               
            }
        });
});

$("#btn_clearnewidproof").click(function(){
	window.location='idproofs';
});
//Create new role user map
$("#btn_addnewuserrole").click(function(){
	debugger;
	var ru_uname=document.getElementById('ru_uname').value;
	var ru_pswd=document.getElementById('ru_pswd').value;
	var ru_roleddl=document.getElementById('ru_roleddl').value;
	var ru_email=document.getElementById('ru_email').value;
		
    $.ajax({
            type: 'GET',
            url: '/mapnewuserrole',
            data: {
			'ru_uname':ru_uname,
			'ru_pswd':ru_pswd,
			'ru_roleddl':ru_roleddl,
			'ru_email':ru_email
			},
            dataType:"json",
            success: function(data) {
				alert(data);	
				window.location='roleuseraccount';			
            },
			 error: function(data) {
               
            }
        });
});
$("#btn_clearnewuserrole").click(function(){
	window.location='roleuseraccount';
});

$("#btn_clearmenumap").click(function(){
	window.location='rolemenumap';
});


$("#btn_clearempcat").click(function(){
	window.location='empcat';
});


function addSrcRow(tableID,data) {  
	debugger;
	
	var table = document.getElementById(tableID);  
	var body = table.createTBody();
	var dataarray = data.split("#");
	for(var m=0;m<dataarray.length;m++)
	{
		var rowdata=dataarray[m];
		var rowdataarray = rowdata.split(",");
		 
		var rowCount = 0;//table.rows.length;  
		//var row = table.insertRow(rowCount);
		var row = body.insertRow(rowCount);
		//for(var n=0;n<rowdataarray.length;n++)
		{
		 
			//Column 1  
			var cell1 = row.insertCell(0); 
			cell1.innerHTML = rowdataarray[0]; 
			
			//Column 2  
			cell1 = row.insertCell(1); 
			cell1.innerHTML = rowdataarray[1]; 
			
			//Column 2  
			cell1 = row.insertCell(2); 
			cell1.innerHTML = rowdataarray[2]; 
			
			//Column 2  
			cell1 = row.insertCell(3); 
			cell1.innerHTML = rowdataarray[3]; 
			
			//Column 2  
			cell1 = row.insertCell(4); 
			cell1.innerHTML = rowdataarray[4]; 
			
			//Column 2  
			cell1 = row.insertCell(5); 
			cell1.innerHTML = rowdataarray[5]; 
			
			//Column 2  
			var cell2 = row.insertCell(6); 
			cell2.innerHTML = rowdataarray[6]; 
			

			var cell2 = row.insertCell(7); 
			cell2.innerHTML = "<a onclick='editempcat("+rowdataarray[0]+",\""+rowdataarray[1]+"\",\""+rowdataarray[2]+"\",\""+rowdataarray[3]+"\",\""+rowdataarray[4]+"\",\""+rowdataarray[5]+"\",\""+rowdataarray[6]+"\")'><i class='fa fa-edit' aria-hidden='true'></i></a>"; 
			
			//Column 3  
			var cell3 = row.insertCell(8); 
			cell3.innerHTML = "<a href='deleteempcat?id="+rowdataarray[0]+"'> <i class='fa fa-trash' aria-hidden='true' style='color:red'></i></a>"; 
			
			
		}
	}
	
	 
}

function editempcat(id,cname,acolor,hdtime,hdcolor,fdtime,fdcolor)
{
	document.getElementById('cname').value=cname.trim();
	document.getElementById('catid').value=id;
	document.getElementById('acolor').value=acolor.trim();
	document.getElementById('hdtime').value=hdtime.trim();
	document.getElementById('hdcolor').value=hdcolor.trim();
	document.getElementById('fdtime').value=fdtime.trim();
	document.getElementById('fdcolor').value=fdcolor.trim();
	document.getElementById('btn_saveempcat').value="Update Category";
}




//Shift Timing
$("#btn_saveempcat").click(function(){
	debugger;
	var btnnm=document.getElementById('btn_saveempcat').value;
	var cname=document.getElementById('cname').value;
	var catid=document.getElementById('catid').value;
	var acolor=document.getElementById('acolor').value;
	var hdtime=document.getElementById('hdtime').value;
	var hdcolor=document.getElementById('hdcolor').value;
	var fdtime=document.getElementById('fdtime').value;
	var fdcolor=document.getElementById('fdcolor').value;
	var stype='';
	if(btnnm=="Add Emp Category")
	{
		stype='New';
	}
	else{
		stype='Update';
	}
		
    $.ajax({
            type: 'GET',
            url: '/addempcat',
            data: {
			'empcat':cname,
			'catid':catid,
			'acolor':acolor,
			'hdtime':hdtime,
			'hdcolor':hdcolor,
			'fdtime':fdtime,
			'fdcolor':fdcolor,
			'type':stype
			},
            dataType:"json",
            success: function(data) {
				if(data!="")
				{
					document.getElementById("empcattable").innerHTML="";
					var table = document.getElementById("empcattable");					
					var header = table.createTHead();
					header.className="bg-darkblue text-white border-darkblue";
					var row = header.insertRow(0);
					row.className="fs-7";
					var cell = row.insertCell(0);
					cell.innerHTML = "<b>Id</b>";
					cell = row.insertCell(1);
					cell.innerHTML = "<b>Category Name</b>";
					cell = row.insertCell(2);
					cell.innerHTML = "<b>Absent Color</b>";
					cell = row.insertCell(3);
					cell.innerHTML = "<b>Half Day Time</b>";
					cell = row.insertCell(4);
					cell.innerHTML = "<b>Half Day Color</b>";
					cell = row.insertCell(5);
					cell.innerHTML = "<b>Full Day Time</b>";
					cell = row.insertCell(6);
					cell.innerHTML = "<b>Full Day Color</b>";
					cell = row.insertCell(7);
					cell.innerHTML = "<b>Edit</b>";
					cell = row.insertCell(8);
					cell.innerHTML = "<b>Delete</b>";
					data=data.replace("\"","");	
					data=data.substr(0,data.length-1);
					addSrcRow('empcattable',data);
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
	var body = table.createTBody();
	var dataarray = data.split("#");
	for(var m=0;m<dataarray.length;m++)
	{
		var rowdata=dataarray[m];
		var rowdataarray = rowdata.split(",");
		 
		var rowCount = 0;//table.rows.length;  
		//var row = table.insertRow(rowCount);
		var row = body.insertRow(rowCount);
		//for(var n=0;n<rowdataarray.length;n++)
		{
		 
			//Column 1  
			var cell1 = row.insertCell(0); 
			cell1.innerHTML = rowdataarray[0]; 
			
			//Column 2  
			cell1 = row.insertCell(1); 
			cell1.innerHTML = rowdataarray[1]; 
			
			//Column 2  
			cell1 = row.insertCell(2); 
			cell1.innerHTML = rowdataarray[2]; 
			
			//Column 2  
			cell1 = row.insertCell(3); 
			cell1.innerHTML = rowdataarray[3]; 
			
			//Column 2  
			cell1 = row.insertCell(4); 
			cell1.innerHTML = rowdataarray[4]; 
			
			//Column 2  
			cell1 = row.insertCell(5); 
			cell1.innerHTML = rowdataarray[5]; 
			
			//Column 2  
			var cell2 = row.insertCell(6); 
			cell2.innerHTML = rowdataarray[6]; 
			

			var cell2 = row.insertCell(7); 
			cell2.innerHTML = "<a onclick='editempcat("+rowdataarray[0]+",\""+rowdataarray[1]+"\",\""+rowdataarray[2]+"\",\""+rowdataarray[3]+"\",\""+rowdataarray[4]+"\",\""+rowdataarray[5]+"\",\""+rowdataarray[6]+"\")'><i class='fa fa-edit' aria-hidden='true'></i></a>"; 
			
			//Column 3  
			var cell3 = row.insertCell(8); 
			cell3.innerHTML = "<a href='deleteempcat?id="+rowdataarray[0]+"'> <i class='fa fa-trash' aria-hidden='true' style='color:red'></i></a>"; 
			
			
		}
	}
	
	 
}

function editempcat(id,cname,acolor,hdtime,hdcolor,fdtime,fdcolor)
{
	document.getElementById('cname').value=cname.trim();
	document.getElementById('catid').value=id;
	document.getElementById('acolor').value=acolor.trim();
	document.getElementById('hdtime').value=hdtime.trim();
	document.getElementById('hdcolor').value=hdcolor.trim();
	document.getElementById('fdtime').value=fdtime.trim();
	document.getElementById('fdcolor').value=fdcolor.trim();
	document.getElementById('btn_saveempcat').value="Update Category";
}



//Shift Timing
$("#btn_createpayroll").click(function(){
	debugger;
	var emplyrpf=document.getElementById('emplyrpf').value;
	var emppf=document.getElementById('emppf').value;
	var emplyresic=document.getElementById('emplyresic').value;
	var empesic=document.getElementById('empesic').value;
	var pt=document.getElementById('pt').value;
	var smon=document.getElementById('smon').value;
	var syear=document.getElementById('syear').value;
	var odeduc=document.getElementById('odeduc').value;
	window.location="payrollupdate?emplyrpf="+emplyrpf+"&emppf="+emppf+"&emplyresic="+emplyresic+"&empesic="+empesic+"&pt="+pt+"&smon="+smon+"&syear="+syear+"&odeduc="+odeduc;
	/*
    $.ajax({
            type: 'GET',
            url: '/payrollupdate',
            data: {
			'emplyrpf':emplyrpf,
			'emppf':emppf,
			'emplyresic':emplyresic,
			'empesic':empesic,
			'pt':pt,
			'smon':smon,
			'syear':syear,
			'odeduc':odeduc
			},
            dataType:"json",
            success: function(data) {
					alerter('Payroll data updated');				
            },
			 error: function(data) {
               
            }
        });
	*/
	
});

function alerter(data)
{
	debugger;
	alert(data);
}



$("#btn_addselemp").click(function(){
	debugger;
	//var baseemplist=document.getElementById('baseemplist').value;
	var baseemplist = document.getElementById('baseemplist');
    var selected = [...baseemplist.options]
                    .filter(option => option.selected)
                    .map(option => option.value);
	var selemplist = document.getElementById('selemplist');
	var selval=selected;
	for (var i = 0; i<selval.length; i++){
		var opt = document.createElement('option');
		opt.value = selval[i];
		opt.innerHTML = selval[i];
		selemplist.appendChild(opt);
	}
    //alert(selected);
	/*
	var emppf=document.getElementById('emppf').value;
	var emplyresic=document.getElementById('emplyresic').value;
	var empesic=document.getElementById('empesic').value;
		
    $.ajax({
            type: 'GET',
            url: '/payrollupdate',
            data: {
			'emplyrpf':emplyrpf,
			'emppf':emppf,
			'emplyresic':emplyresic,
			'empesic':empesic
			},
            dataType:"json",
            success: function(data) {
					alerter('Payroll data updated');				
            },
			 error: function(data) {
               
            }
        });
	*/
	
});

$("#btn_remselemp").click(function(){
	debugger;
	var selemplist = document.getElementById("selemplist");
        var options = selemplist.options;
        var i = options.length;
        while (i--) {
            var current = options[i];
            if (current.selected) {
                // Do something with the selected option
                current.parentNode.removeChild(current);
            }
		}
	
});


$("#btn_remgendates").click(function(){
	debugger;
	var selemplist = document.getElementById("seldates");
        var options = selemplist.options;
        var i = options.length;
        while (i--) {
            var current = options[i];
                current.parentNode.removeChild(current);
		}
	
});



//Rostering fetch emp on proc
function fetchprocwiseemp()
{
	debugger;
	var procname=document.getElementById('proclist').value;
		
    $.ajax({
            type: 'GET',
            url: '/fetchemponproc',
            data: {
			'procname':procname
			},
            dataType:"json",
            success: function(data) {
					updatebaseemp(data)
            },
			 error: function(data) {
               
            }
        });
	
	
}

function updatebaseemp(data)
{
		debugger;
		//alert(data)			
		var dataarray = data.split("#");
		var baseemplist = document.getElementById('baseemplist');
		baseemplist.innerHTML="";
		for(var i=0;i<dataarray.length;i++)
		{
			var rowdataarray = dataarray[i].split(",");
			var opt = document.createElement('option');
			opt.value = rowdataarray[0]+"-"+rowdataarray[1];
			opt.innerHTML = rowdataarray[0]+"-"+rowdataarray[1];
			baseemplist.appendChild(opt);
		}			
}




$("#btn_rosgendates").click(function(){
	debugger;
	//var baseemplist=document.getElementById('baseemplist').value;
	var sdate = document.getElementById('sdate').value;
	var edate = document.getElementById('edate').value;    
	let dates = []
	  //to avoid modifying the original date
	const theDate = new Date(sdate)
	edate = new Date(edate)
	  while (theDate < edate) {
		dates = [...dates, new Date(theDate)]
		theDate.setDate(theDate.getDate() + 1)
	  }
	  dates = [...dates, edate]
	  
		var seldates = document.getElementById('seldates');
		for(var i=0;i<dates.length;i++)
		{
			var opt = document.createElement('option');
			opt.value = dates[i].toLocaleDateString("en-US");
			opt.innerHTML = dates[i].toLocaleDateString("en-US");
			seldates.appendChild(opt);
		}	
	
});

function addtosellist()
{
	var inddate = document.getElementById('inddate').value;   
	inddate = new Date(inddate)
		var seldates = document.getElementById('seldates');
	var opt = document.createElement('option');
			opt.value = inddate.toLocaleDateString("en-US");
			opt.innerHTML = inddate.toLocaleDateString("en-US");
	seldates.appendChild(opt);
}




  
 
 

//Rostering Save data
$("#btn_savrostdata").click(function(){
	debugger;
	var emplist = document.getElementById('selemplist');
    var selectedemp = [...emplist.options]
                    .filter(option => option.selectedemp)
                    .map(option => option.value);
	selectedemp=GetSelectValues(emplist);
	var selempval='';
	for (var i = 0; i<selectedemp.length; i++){
		selempval=selempval+selectedemp[i];
	}
	
	var dateslist = document.getElementById('seldates');
    var selecteddates = [...dateslist.options]
                    .filter(option => option.selecteddates)
                    .map(option => option.value);
	
	selecteddates=GetSelectValues(dateslist);
	var seldatesval='';
	for (var i = 0; i<selecteddates.length; i++){
		seldatesval=seldatesval+selecteddates[i];
	}
	
	 
	var sdate = document.getElementById('sdate').value;
	var edate = document.getElementById('edate').value;  
	var proc = document.getElementById('proclist').value;
	
	
	var ltype = document.getElementById('ltype').value;   
	var stype = document.getElementById('stype').value; 

	 $.ajax({
            type: 'GET',
            url: '/setuprostering',
            data: {
			'selectedemp':selempval,
			'selecteddates':seldatesval,
			'ltype':ltype,
			'stype':stype
			},
            dataType:"json",
            success: function(data) {
				if(data=="")
				{
					alert("Allocation successfull");
				}
				else
				{
					alert(data);	
				}
					alerter('Rostering completed');			
					window.location="rostering";	
            },
			 error: function(data) {
               
            }
});
});


function GetSelectValues(select) {
  var result = [];
  var options = select && select.options;
  var opt;

  for (var i=0, iLen=options.length; i<iLen; i++) {
    opt = options[i];
      result.push(opt.value+"," || opt.text+",");
  }
  return result;
}


//Savepref

$("#btn_saveoecpref").click(function(){
	debugger;
	var numberOfChecked = $("#upload-file").find("input[type=checkbox]:checked").length
	if(numberOfChecked==5)
	{
		if (confirm("Are you Sure about your preference selection")) {
			
		 
			var form_data = new FormData($('#upload-file')[0]);
					$.ajax({
						type: 'POST',
						url: '/uploadpref',
						data: form_data,
						contentType: false,
						cache: false,
						processData: false,
						success: function(data) {
							console.log('Success!');
							alert('OEC Preferences stored successfully');
							window.location='schooseelectives';
						},
					});
		} 
	else {
		alert("Please check your preferences");
	  }
	}
	else{
		alert('You have to choose 5 preferences only');
	}
});

//load student data
$("#btn_loadstudata").click(function(){
	debugger;
   var form_data = new FormData($('#upload-file')[0]);
        $.ajax({
            type: 'POST',
            url: '/uploadstudentdata',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(emotion) {
				//alerter(emotion);
                console.log('Success!');
				alert('Data stored successfully');
            },
        });
});


$("#btn_clearstudata").click(function(){
	var form_data = new FormData($('#upload-file')[0]);
		 $.ajax({
			 type: 'POST',
			 url: '/cleardataset',
			 data: form_data,
			 contentType: false,
			 cache: false,
			 processData: false,
			 success: function(data) {
				 console.log('Success!');
				 alert('Dataset has been cleared');
			 },
		 });
 });

 
//load hod data
$("#btn_loadhodata").click(function(){
	debugger;
   var form_data = new FormData($('#upload-file')[0]);
        $.ajax({
            type: 'POST',
            url: '/uploadhoddata',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(emotion) {
				//alerter(emotion);
                console.log('Success!');
				alert('Data stored successfully');
            },
        });
});


$("#btn_clearhoddata").click(function(){
	var form_data = new FormData($('#upload-file')[0]);
		 $.ajax({
			 type: 'POST',
			 url: '/clearhoddataset',
			 data: form_data,
			 contentType: false,
			 cache: false,
			 processData: false,
			 success: function(data) {
				 console.log('Success!');
				 alert('Dataset has been cleared');
			 },
		 });
 });

 
$("#btn_savepecpref").click(function(){
	debugger;
	var numberOfChecked =$("#upload-file1").find("input[type=checkbox]:checked").length
	if(numberOfChecked==1)
	{
		if (confirm("Are you Sure about your preference selection")) {
			
		 
			var form_data = new FormData($('#upload-file1')[0]);
					$.ajax({
						type: 'POST',
						url: '/uploadpref1',
						data: form_data,
						contentType: false,
						cache: false,
						processData: false,
						success: function(data) {
							console.log('Success!');
							alert('PEC Preferences stored successfully');
							window.location='schooseelectives';
						},
					});
		} 
	else {
		alert("Please check your preferences");
	  }
	}
	else{
		alert('You have to choose 1 preferences only');
	}
});


//Role Menu Map
function rolesmap()
{
	debugger;
	if(document.getElementById('roleddl').value=='Admin')
	{
		for(i=1;i<=36;i++)
		{
			document.getElementById('menu_'+i).checked=false;
		}
		for(i=1;i<=36;i++)
		{
			document.getElementById('menu_'+i).checked=true;
		}
	}
	else if(document.getElementById('roleddl').value=='HR Manager')
	{
		for(i=1;i<=36;i++)
		{
			document.getElementById('menu_'+i).checked=false;
		}
		for(i=1;i<=33;i++)
		{
			document.getElementById('menu_'+i).checked=true;
		}
		document.getElementById('menu_36').checked=true;
	}
	else if(document.getElementById('roleddl').value=='HR Operations')
	{
		for(i=1;i<=36;i++)
		{
			document.getElementById('menu_'+i).checked=false;
		}
		for(i=1;i<=8;i++)
		{
			document.getElementById('menu_'+i).checked=true;
		}
		document.getElementById('menu_11').checked=true;
		document.getElementById('menu_13').checked=true;
		document.getElementById('menu_14').checked=true;
		document.getElementById('menu_15').checked=true;
		document.getElementById('menu_18').checked=true;
		document.getElementById('menu_20').checked=true;
		for(i=24;i<=33;i++)
		{
			document.getElementById('menu_'+i).checked=true;
		}
		document.getElementById('menu_36').checked=true;
	}
	else if(document.getElementById('roleddl').value=='Recruiter' || document.getElementById('roleddl').value=='Recruitment Manager')
	{
		for(i=1;i<=36;i++)
		{
			document.getElementById('menu_'+i).checked=false;
		}
		document.getElementById('menu_4').checked=true;
	}
	else if(document.getElementById('roleddl').value=='Operations Manager')
	{
		for(i=1;i<=36;i++)
		{
			document.getElementById('menu_'+i).checked=false;
		}
		document.getElementById('menu_7').checked=true;
		document.getElementById('menu_8').checked=true;
		document.getElementById('menu_4').checked=true;
	}
	
	else if(document.getElementById('roleddl').value=='Employee')
	{
		for(i=1;i<=36;i++)
		{
			document.getElementById('menu_'+i).checked=false;
		}
		document.getElementById('menu_7').checked=true;
	}
	else{
		for(i=1;i<=36;i++)
		{
			document.getElementById('menu_'+i).checked=false;
		}
	}
}
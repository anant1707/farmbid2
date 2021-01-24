const canvas=document.getElementById("line-input");
const txtarea=document.getElementById("txtarea");
const ctx=canvas.getContext("2d");



canvas.width=window.innerWidth-8;
canvas.height=(window.innerHeight * 0.5);
txtarea.style.setProperty('width',`${window.innerWidth-15}px`,'');
txtarea.style.setProperty('height',`${window.innerHeight-canvas.height}px`,'');

alert("Shortcuts\n1. Undo- Ctrl+Z\n2. Redo- Ctrl+Y \n3. Clear all- Ctrl+delete");

var is_drawing=false;

// Containers for storing coordinates
var points=[];
var redo_stack=[];
var current_stroke=[];


//Setting Default
var eraser_size=5//default
var pen_colour="#000000";
var pen_size=3;
ctx.lineWidth=pen_size;//default
ctx.lineCap="round";
ctx.strokeStyle=pen_colour;//default
ctx.lineJoin='round';

function mouse_start_draw(e)
{
   is_drawing=true;
   ctx.beginPath();
   redo_stack=[];
   current_stroke.push
   (
      {
         x:e.offsetX,
         y:e.offsetY
      }
   );

}

function mouse_stop_draw(e)
{
   is_drawing=false;

   points.push(current_stroke);
   current_stroke=[];
}

function mouse_draw(e)
{
   if(!is_drawing)
   return;

    current_stroke.push
   (
      {
         x:e.offsetX,
         y:e.offsetY
      }
   );

   ctx.lineTo(e.offsetX,e.offsetY);
   ctx.stroke();
   

}

function undo()
{
   if(points.length<1)
   return;

   var last_stroke=points.pop();
   redo_stack.push(last_stroke);
   redraw_all();
   
}

function redo()
{
   if(redo_stack.length<1)
   return;
   var last_stroke=redo_stack.pop();
   points.push(last_stroke);
   redraw_all();
}

function redraw_all()
{
   ctx.clearRect(0,0,canvas.width,canvas.height);
   for (var i=0; i<points.length; i++)
   {
      ctx.beginPath();
      for (var c=0;c<points[i].length;c++)
      {
         ctx.lineTo(points[i][c].x,points[i][c].y);
         ctx.stroke();
      }
   }
}

function ClearAll()
{
   ctx.clearRect(0,0,canvas.width,canvas.height);
   points=[];
}

function convert()
{
   fetch('/RTHWR',{
      method:"POST",
      headers: {
         "content-type":"application/json"
      },
      body:JSON.stringify(points)
   }).then(function (response) { // At this point, Flask has printed our JSON
      return response.text();
  }).then(function (text) {
   
   
      var ttn=txtarea.innerHTML;
      ttn+=text;
      txtarea.innerHTML=ttn;
  });
}

function shortcuts(e)
{
   if(e.ctrlKey && e.keyCode==90)
   {
      undo();
   }
   if(e.ctrlKey && e.keyCode==89)
   {
      redo();
   }
   if(e.ctrlKey && e.keyCode==46)
   {
      ClearAll();
   } 
   if(e.keyCode==32)
   {
      convert();
      ClearAll();
   }
}

canvas.addEventListener("mousedown",mouse_start_draw);
canvas.addEventListener("mouseup",mouse_stop_draw);
canvas.addEventListener("mousemove",mouse_draw);
canvas.addEventListener("mouseenter",function()
{
   
      canvas.style.setProperty("cursor","url('static/external/CURSORS/dot.cur'), auto","")
})
document.addEventListener('keyup',shortcuts,false);
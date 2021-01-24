
const canvas=document.getElementById("mainboard");
const ctx=canvas.getContext("2d");;
var tcanvas = document.createElement('canvas');
var tctx = tcanvas.getContext('2d');
canvas.width=tcanvas.width=window.innerWidth;
canvas.height=tcanvas.height=window.innerHeight;
tcanvas.id = 'tcanvas';
tcanvas.style="position:fixed";
sketching_area.appendChild(tcanvas);
var is_drawing=false;
var pen=true;
var eraser_size=5//default

ctx.lineWidth=5;//default
ctx.strokeStyle="black";//default
function start_draw()
{
   is_drawing=true;
   ctx.beginPath();
}
function stop_draw()
{
   is_drawing=false;
   ctx.beginPath();

}
function draw(e)
{
   if(!is_drawing)
   return;

   if(pen)
   {
   ctx.lineTo(e.clientX,e.clientY);
   ctx.stroke();
   }
   else
   {
      ctx.clearRect(e.clientX-eraser_size,e.clientY-eraser_size,eraser_size,eraser_size);
   }
}
function select_eraser(t)
{
   pen=false;
   eraser_size=t;
}

function select_pen(t)
{
   pen=true;
   ctx.lineWidth=t;
}
function ClearAll()
{
   ctx.clearRect(0,0,canvas.width,canvas.height);
}
function changeColor(t)
{
   ctx.strokeStyle=t;
}
canvas.addEventListener("mousedown",start_draw);
canvas.addEventListener("mouseup",stop_draw);
canvas.addEventListener("mousemove",draw);


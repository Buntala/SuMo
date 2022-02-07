function graph_plot(clicked_name){
    var img = document.getElementById("hello");
    img.style.display="block";
    img.src = '/plot.png/'+ clicked_name;
}
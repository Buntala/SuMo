function graph_plot(clicked_id){
    var img = document.getElementById("hello");
    img.style.display="block";
    img.src = '/plot.png/'+ clicked_id;
}
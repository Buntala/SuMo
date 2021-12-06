function graph_plot(clicked_id){
    var img = document.getElementById("hello");
    img.src = '/plot.png/'+ clicked_id;
    document.getElementById('body').appendChild(img);
}
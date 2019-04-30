var height = 400;
var width = 800;
var margin = 40;

function fetch_data() {
  var username = $("#username").val();
  var password = $("#password").val();
  function onSuccess(data){
    plot_holdings_vis(data);
  }

  get_dashboard_data(username, password, onSuccess); //in static/requests.js 

}

function plot_holdings_vis(data) {
  var labelX = 'Market Cap';
  var labelY = 'P/E';
  var svg = d3.select('.chart')
              .append('svg')
              .attr('class', 'chart')
              .attr("width", width + margin + margin)
              .attr("height", height + margin + margin)
              .append("g")
              .attr("transform", "translate(" + margin + "," + margin + ")");
                      
  var x = d3.scale.linear()
            .domain(d3.extent(data, function(d) {return d.market_cap; })).nice()
            .range([0, width]);

  var y = d3.scale.linear()
            .domain([d3.min(data, function (d) { return d.pe_ratio; })-9, d3.max(data, function (d) { return d.pe_ratio; })])
            .range([height, 0]);

  var scale = d3.scale.sqrt()
                .domain([d3.min(data, function (d) { return d.holding_val; }), d3.max(data, function (d) { return d.holding_val; })])
                .range([1, 20]);

  var opacity = d3.scale.sqrt()
                  .domain([d3.min(data, function (d) { return d.holding_val; }), d3.max(data, function (d) { return d.holding_val; })])
                  .range([1, .5]);
                                  
  var color = d3.scale.category20();

  formatValue = d3.format(".2s");
  var xAxis = d3.svg.axis().scale(x).tickFormat(function(d) { return formatValue(d).replace('G', 'B'); });
  var yAxis = d3.svg.axis().scale(y).ticks(6).orient("left");
   
  svg.append("g")
     .attr("class", "y axis")
     .call(yAxis)
     .append("text")
     .attr("transform", "rotate(-90)")
     .attr("x", 20)
     .attr("y", -margin)
     .attr("dy", ".71em")
     .style("text-anchor", "end")
     .text(labelY);
          
  // x axis and label
  svg.append("g")
     .attr("class", "x axis")
     .attr("transform", "translate(0," + height + ")")
     .call(xAxis)
     .append("text")
     .attr("x", width + 20)
     .attr("y", margin - 10)
     .attr("dy", ".71em")
     .style("text-anchor", "end")
     .text(labelX);

  svg.append("line")
     .style("stroke-dasharray", ("3, 3"))
     .style("stroke", "rgb(155, 154, 154)")
     .attr("x1", x(0))
     .attr("y1", y(0))
     .attr("x2", width/2-15)
     .attr("y2", y(0))
     
  svg.append("line")
     .style("stroke-dasharray", ("3, 3"))
     .style("stroke", "rgb(155, 154, 154)")
     .attr("x1", width/2+99)
     .attr("y1", y(0))
     .attr("x2", width)
     .attr("y2", y(0))
     
  svg.append("text")
     .attr("id", "marker")
     .attr("transform", "translate(" + (width/2) + "," + y(0) + ")")
     .attr("dy", ".35em")
     .attr("text-anchor", "start")
     .text("Lossing Money");

  var tooltip = d3.select(".chart")
                  .append("div")
                  .style("position", "absolute")
                  .style("opacity", 0)
                  .attr("class", "tooltip")
                  
  svg.selectAll("circle")
    .data(data)
    .enter()
    .insert("circle")
    .attr("cx", width / 2)
    .attr("cy", height / 2)
    .attr("id", height / 2)
    .attr("opacity", function (d) { return opacity(d.holding_val); })
    .attr("r", function (d) { return scale(d.holding_val); })
    .style("fill", function (d) { return color(d.sector); })
    .on('mouseover', function (d, i) {
        fade(d.sector, .1);
        tooltip_mouseover(d);
    })
   .on('mouseout', function (d, i) {
       fadeOut();
       tooltip_mouseout();
   })
   .transition()
   .delay(function (d, i) { return x(d.market_cap) - y(d.pe_ratio); })
   .duration(500)
   .attr("cx", function (d) { return x(d.market_cap); })
   .attr("cy", function (d) { return y(d.pe_ratio); })
   .ease("bounce");

  function tooltip_mouseover(d) {
      tooltip.style("opacity", 0.9)
             .html("<span class='title'>" + d.name + " (" + d.port_percent.toFixed(2) + "%)</span>" + 
                   "<br>" + d.sector + " (" + d.sector_port_percent.toFixed(2) + "%)" +
                   "<br>Price: " + d.last_trade_price + "     Quantity: " + d.quantity_held)
             .style("left", (event.pageX+10) + "px")
             .style("top", (event.pageY-20) + "px");
  }

  function tooltip_mouseout() {
      tooltip.style("opacity", 0);
  }
                               
  function fade(sector, opacity) {
    svg.selectAll("circle")
       .filter(function (d) {
            return d.sector != sector;
        })
       .transition()
       .style("opacity", opacity);
  }

  function fadeOut() {
    svg.selectAll("circle")
       .transition()
       .style("opacity", function (d) { opacity(d.holding_val); });
  }
}
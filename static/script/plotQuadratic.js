function plotQuadratic(plot_info, plot_array,expression) {
  const output = document.querySelector('.output-pane')

  // Prepare the trace for the quadratic curve
  const trace = {
    x: plot_array.x,
    y: plot_array.y,
    mode: 'lines',
    name: 'Quadratic Curve',
    line: { color: 'blue' }
  };

  // Prepare markers for roots, vertex, and y-intercept
  const markers1 = [
    {
      x: [plot_info.root1.real],
      y: [0],
      mode: 'markers',
      name: `Root 1 : (${plot_info.root1.real})` ,
      marker: { color: 'red', size: 10 }
    },
    {
      x: [plot_info.root2.real],
      y: [0],
      mode: 'markers',
      name: `Root 2 : (${plot_info.root2.real})`,
      marker: { color: 'red', size: 10 }
    },
  ]
  const markers2 = [
    {
      x: [plot_info.vertex[0]],
      y: [plot_info.vertex[1]],
      mode: 'markers',
      name: `Vertex : (${plot_info.vertex[0]}, ${plot_info.vertex[1]})`,
      marker: { color: 'green', size: 12, symbol: 'diamond' }
    },
    {
      x: [0],
      y: [plot_info.y_intercept],
      mode: 'markers',
      name: `Y-Intercept : (${plot_info.y_intercept})`,
      marker: { color: 'orange', size: 10,symbol: 'cross'}
    }
  ];
  

  let data;
  
  if (plot_info.root1.imag == 0 && plot_info.root2.imag == 0 ) {
    data = [trace, ...markers1, ...markers2];
  } else {
    data = [trace, ...markers2];
  }
  const layout = {
    title: `Plot : ${expression}`,
    showlegend: true,
    legend: {
      orientation: "h",
    },
    height:600,
    autosize: true,
  };

  output.innerHTML += `
    <div class="box-styling" id="graphContent" style="width:100%;"></div>
    `
  Plotly.newPlot('graphContent', data, layout);
}
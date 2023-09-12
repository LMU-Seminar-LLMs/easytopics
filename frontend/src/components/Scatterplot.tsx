import React, { useState } from 'react';
import Plot from 'react-plotly.js';
import ScatterOverlay from './ScatterOverlay.tsx';
import { Data1Scatter, Data2Scatter } from '../data/example_scatter.tsx';

type DataPoint = {
  x: number;
  y: number;
};

type Series = {
  name: string;
  data: DataPoint[];
};

function transformData(
  name: string,
  inputData: { x: number[]; y: number[] }
): Series {
  const { x, y } = inputData;
  const dataPoints: DataPoint[] = [];

  for (let i = 0; i < x.length; i++) {
    dataPoints.push({ x: x[i], y: y[i] });
  }

  return {
    name: name,
    data: dataPoints,
  };
}

const Scatterplot: React.FC = () => {
  const [series, setSeries] = useState<Series[]>([
    transformData('Series 1', Data1Scatter),
    transformData('Series 2', Data2Scatter),
  ]);

  const [showOverlay, setShowOverlay] = useState(false);
  const [overlayContent, setOverlayContent] = useState<string>('');

  const plotlyData = series.map((s) => ({
    x: s.data.map((point) => point.x),
    y: s.data.map((point) => point.y),
    mode: 'markers',
    type: 'scatter',
    name: s.name,
    opacity: 0.6,
    marker: {
      size: 5,
      line: {
        width: 1,
        color: 'black',
      },
    },
  }));

  const handlePointClick = (data: any) => {
    const clickedSeriesName = data.points[0].data.name;
    const clickedX = data.points[0].x;
    const clickedY = data.points[0].y;

    setOverlayContent(
      `Clicked on ${clickedSeriesName} at point (x: ${clickedX}, y: ${clickedY})`
    );
    setShowOverlay(true);
  };

  const [plotLayout, setPlotLayout] = useState({
    title: false,
    showlegend: true,
    autosize: true,
    autoscale: false,
    width: window.innerWidth * 0.75,
    height: window.innerHeight * 0.75,
    scattermode: 'overlay',
    xaxis: {
      //visible: false,
      zeroline: true,
    },
    yaxis: {
      zeroline: true,
    },
    marker: {
      opacity: 0.9,
    },
  });

  const handleRelayout = (newLayout: any) => {
    // On relayout event (like zooming), update the state
    setPlotLayout((prevLayout) => ({
      ...prevLayout,
      ...newLayout,
    }));
  };

  return (
    <div className='p-4 border mx-0 bg-white'>
      <Plot
        data={plotlyData}
        layout={plotLayout}
        onRelayout={handleRelayout}
        onClick={handlePointClick}
        config={{
          displayModeBar: true,
          modeBarButtonsToRemove: [
            'zoom2d',
            'pan2d',
            'select2d',
            'lasso2d',
            'zoomIn2d',
            'zoomOut2d',
            'autoScale2d',
            'resetScale2d',
          ],
          toImageButtonOptions: {
            format: 'svg',
          },
          scrollZoom: true,
          responsive: true,
        }}
      />
      {showOverlay && (
        <ScatterOverlay
          content={overlayContent}
          onClose={() => setShowOverlay(false)}
        />
      )}
    </div>
  );
};

export default Scatterplot;

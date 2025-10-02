import React from 'react';
import Plot from 'react-plotly.js';

const McCabeThielePlot = ({ data, isStripping = false }) => {
    if (!data) {
        return <div>No data available for plot.</div>;
    }

    const { eq_x, eq_y, op_x, op_y } = data;

    const layout = {
        xaxis: {
            title: isStripping ? 'Organic Cu Concentration (g/L)' : 'Aqueous Cu Concentration (g/L)',
            gridcolor: '#f0f0f0',
        },
        yaxis: {
            title: isStripping ? 'Aqueous Cu Concentration (g/L)' : 'Organic Cu Concentration (g/L)',
            gridcolor: '#f0f0f0',
        },
        margin: { t: 40, b: 40, l: 60, r: 20 },
        showlegend: true,
        legend: {
            x: 0.05,
            y: 0.95,
            bgcolor: 'rgba(255, 255, 255, 0.5)',
            bordercolor: '#ddd',
            borderwidth: 1
        },
        plot_bgcolor: '#fff',
        paper_bgcolor: '#fff',
        autosize: true,
    };

    const plotData = [
        {
            x: eq_x,
            y: eq_y,
            mode: 'lines',
            name: 'Equilibrium Line',
            line: { color: '#1890ff', width: 3 }
        },
        {
            x: op_x,
            y: op_y,
            mode: 'lines+markers',
            name: 'Operating Line',
            line: { color: '#ff4d4f', width: 2, dash: 'dash' },
            marker: { size: 8 }
        }
    ];

    return (
        <Plot
            data={plotData}
            layout={layout}
            useResizeHandler={true}
            style={{ width: '100%', height: '100%' }}
            config={{ responsive: true }}
        />
    );
};

export default McCabeThielePlot;
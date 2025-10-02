import React from 'react';
import { Card, Row, Col, Typography } from 'antd';
import { ArrowRightOutlined } from '@ant-design/icons';

const { Text } = Typography;

const Stream = ({ label, value, unit, top, left }) => (
    <div style={{ position: 'absolute', top, left, textAlign: 'center', minWidth: '100px' }}>
        <Text strong>{label}</Text><br />
        <Text type="secondary">{value ? `${value.toFixed(2)} ${unit}` : 'N/A'}</Text>
    </div>
);

const MixerSettler = ({ name, top, left }) => (
    <div style={{
        position: 'absolute',
        top,
        left,
        width: '80px',
        height: '80px',
        border: '2px solid #1890ff',
        borderRadius: '8px',
        backgroundColor: '#e6f7ff',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
    }}>
        <Text strong>{name}</Text>
    </div>
);

const FlowArrow = ({ top, left, width = 100, rotate = 0 }) => (
    <div style={{ position: 'absolute', top, left, width, transform: `rotate(${rotate}deg)` }}>
        <ArrowRightOutlined style={{ fontSize: '24px', color: '#595959' }} />
    </div>
);


const FlowsheetDiagram = ({ results }) => {
    const {
        raffinate_E1,
        raffinate_E2,
        C1Cuor_Ext,
        C2Cuor_Ext, // Loaded Organic
        C1Cuor_Str, // Stripped Organic
        AD_Cu,      // Advanced Electrolyte
    } = results;

    // Get PLS and SP values from the detailed results if available, otherwise use a placeholder
    // These values are inputs, so they are not in the main result object but in the 'rest'
    const PLS_Cu = results.PLS_Cu || (results.rest && results.rest.PLS_Cu);
    const SP_Cu = results.SP_Cu || (results.rest && results.rest.SP_Cu);

    return (
        <Card title="Configuration A: 2E + 1S Flowsheet" style={{ minHeight: '500px' }}>
            <div style={{ position: 'relative', height: '450px', width: '100%' }}>
                {/* Extraction Section */}
                <Text strong style={{ position: 'absolute', top: 0, left: '25%' }}>Extraction</Text>
                <MixerSettler name="E2" top={50} left={'calc(50% - 140px)'} />
                <MixerSettler name="E1" top={50} left={'calc(50% + 60px)'} />

                {/* Aqueous Flow (Top) */}
                <Stream label="PLS" value={PLS_Cu} unit="g/L" top={0} left={'calc(50% + 150px)'} />
                <FlowArrow top={65} left={'calc(50% - 40px)'} />
                <Stream label="Raffinate E1" value={raffinate_E1} unit="g/L" top={0} left={'calc(50% - 40px)'} />
                <FlowArrow top={65} left={'calc(50% - 240px)'} />
                <Stream label="Final Raffinate" value={raffinate_E2} unit="g/L" top={0} left={'calc(50% - 350px)'} />


                {/* Organic Flow (Bottom) */}
                <FlowArrow top={155} left={'calc(50% - 240px)'} />
                <Stream label="Stripped Organic" value={C1Cuor_Str} unit="g/L" top={180} left={'calc(50% - 350px)'} />
                <FlowArrow top={155} left={'calc(50% - 40px)'} />
                <Stream label="Org from E2" value={C1Cuor_Ext} unit="g/L" top={180} left={'calc(50% - 40px)'} />
                <Stream label="Loaded Organic" value={C2Cuor_Ext} unit="g/L" top={180} left={'calc(50% + 150px)'} />

                {/* Vertical Arrow to Stripping */}
                <FlowArrow top={200} left={'calc(50% + 180px)'} rotate={90} />


                {/* Stripping Section */}
                <Text strong style={{ position: 'absolute', top: 250, left: '25%' }}>Stripping</Text>
                <MixerSettler name="S1" top={300} left={'calc(50% + 60px)'} />

                {/* Electrolyte Flow */}
                <FlowArrow top={315} left={'calc(50% - 40px)'} />
                <Stream label="Spent Electrolyte" value={SP_Cu} unit="g/L" top={270} left={'calc(50% - 150px)'} />
                <Stream label="Advanced Electrolyte" value={AD_Cu} unit="g/L" top={360} left={'calc(50% - 150px)'} />

                {/* Organic Flow in Stripping */}
                <FlowArrow top={315} left={'calc(50% + 160px)'} rotate={180} />
                <FlowArrow top={250} left={'calc(50% - 120px)'} rotate={-90} />
            </div>
        </Card>
    );
};

export default FlowsheetDiagram;
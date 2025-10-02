import React from 'react';
import { Row, Col, Card, Statistic, Table, Button, Tabs, Divider } from 'antd';
import { FileExcelOutlined, LineChartOutlined, ApartmentOutlined } from '@ant-design/icons';
import McCabeThielePlot from './McCabeThielePlot';
import FlowsheetDiagram from './FlowsheetDiagram';

const { TabPane } = Tabs;

const StatCard = ({ title, value, precision, unit }) => (
    <Card>
        <Statistic
            title={title}
            value={value}
            precision={precision}
            suffix={unit}
        />
    </Card>
);

const OutputPanel = ({ results }) => {
    const {
        success,
        message,
        v_v_percent_opt,
        SR_opt,
        Mef1e_opt,
        Mef2e_opt,
        extraction_recovery,
        stripping_recovery,
        net_transfer,
        mccabe_thiele_extraction,
        mccabe_thiele_stripping,
        ...rest
    } = results;

    // Prepare data for the results table
    const resultData = [
        { key: 'v_v_percent_opt', parameter: 'Optimal Extractant (v/v %)', value: v_v_percent_opt?.toFixed(2) },
        { key: 'SR_opt', parameter: 'Optimal Saturation Ratio (%)', value: SR_opt?.toFixed(2) },
        { key: 'Mef1e_opt', parameter: 'Optimal Mixer Eff. E1 (%)', value: Mef1e_opt?.toFixed(2) },
        { key: 'Mef2e_opt', parameter: 'Optimal Mixer Eff. E2 (%)', value: Mef2e_opt?.toFixed(2) },
        { key: 'extraction_recovery', parameter: 'Extraction Recovery (%)', value: extraction_recovery?.toFixed(2) },
        { key: 'stripping_recovery', parameter: 'Stripping Recovery (%)', value: stripping_recovery?.toFixed(2) },
        { key: 'net_transfer', parameter: 'Net Transfer (g/L per 1% ext.)', value: net_transfer?.toFixed(3) },
        { key: 'raffinate_E2', parameter: 'Final Raffinate Cu (g/L)', value: rest.raffinate_E2?.toFixed(3) },
        { key: 'C2Cuor_Ext', parameter: 'Loaded Organic Cu (g/L)', value: rest.C2Cuor_Ext?.toFixed(3) },
        { key: 'C1Cuor_Str', parameter: 'Stripped Organic Cu (g/L)', value: rest.C1Cuor_Str?.toFixed(3) },
        { key: 'O_A_str', parameter: 'Stripping O/A Ratio', value: rest.O_A_str?.toFixed(2) },
    ].filter(item => item.value !== undefined && item.value !== null);

    const columns = [
        { title: 'Parameter', dataIndex: 'parameter', key: 'parameter' },
        { title: 'Value', dataIndex: 'value', key: 'value' },
    ];

    const handleExport = () => {
        const csvContent = "data:text/csv;charset=utf-8,"
            + "Parameter,Value\n"
            + resultData.map(e => `"${e.parameter}",${e.value}`).join("\n");
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "simulation_results.csv");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    return (
        <div>
            <Row gutter={[16, 16]}>
                <Col xs={24} sm={12} md={8}>
                    <StatCard title="Optimal Extractant" value={v_v_percent_opt} precision={2} unit="v/v %" />
                </Col>
                <Col xs={24} sm={12} md={8}>
                    <StatCard title="Extraction Recovery" value={extraction_recovery} precision={2} unit="%" />
                </Col>
                <Col xs={24} sm={12} md={8}>
                    <StatCard title="Net Transfer" value={net_transfer} precision={3} unit="g/L" />
                </Col>
            </Row>

            <Divider />

            <Tabs defaultActiveKey="1">
                <TabPane
                    tab={<span><ApartmentOutlined />Flowsheet</span>}
                    key="1"
                >
                    <FlowsheetDiagram results={results} />
                </TabPane>
                <TabPane
                    tab={<span><LineChartOutlined />McCabe-Thiele Plots</span>}
                    key="2"
                >
                    <Row gutter={[16, 16]}>
                        <Col xs={24} lg={12}>
                            <Card title="Extraction McCabe-Thiele">
                                {mccabe_thiele_extraction && <McCabeThielePlot data={mccabe_thiele_extraction} />}
                            </Card>
                        </Col>
                        <Col xs={24} lg={12}>
                            <Card title="Stripping McCabe-Thiele">
                                {mccabe_thiele_stripping && <McCabeThielePlot data={mccabe_thiele_stripping} isStripping />}
                            </Card>
                        </Col>
                    </Row>
                </TabPane>
            </Tabs>

            <Divider />

            <Card title="Detailed Simulation Results">
                <Button
                    onClick={handleExport}
                    icon={<FileExcelOutlined />}
                    style={{ marginBottom: 16 }}
                >
                    Export to CSV
                </Button>
                <Table
                    columns={columns}
                    dataSource={resultData}
                    pagination={false}
                    size="small"
                />
            </Card>
        </div>
    );
};

export default OutputPanel;
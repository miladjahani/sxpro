import React, { useState } from 'react';
import { Layout, message, Spin, Alert } from 'antd';
import { SettingOutlined } from '@ant-design/icons';

import InputPanel from './components/InputPanel';
import OutputPanel from './components/OutputPanel';
import { runSimulation } from './api/simulationApi';

const { Header, Sider, Content } = Layout;

const App = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [simulationResults, setSimulationResults] = useState(null);

    const handleRunSimulation = async (formData) => {
        setLoading(true);
        setError(null);
        setSimulationResults(null);
        try {
            const results = await runSimulation(formData);
            if (results.success) {
                message.success('Simulation completed successfully!');
                setSimulationResults(results);
            } else {
                setError(results.message || 'Optimization failed. Please check your inputs.');
                message.error(results.message || 'Optimization failed.');
            }
        } catch (err) {
            setError(err.message || 'An unexpected error occurred.');
            message.error(err.message || 'An unexpected error occurred.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Layout style={{ minHeight: '100vh' }}>
            <Header style={{ background: '#fff', padding: '0 24px', borderBottom: '1px solid #f0f0f0' }}>
                <div style={{ display: 'flex', alignItems: 'center' }}>
                    <SettingOutlined style={{ fontSize: '24px', color: '#1890ff' }} />
                    <h1 style={{ margin: '0 0 0 16px', fontSize: '20px' }}>SimSXCu Web</h1>
                </div>
            </Header>
            <Layout>
                <Sider width={400} theme="light" style={{ padding: '24px', borderRight: '1px solid #f0f0f0' }}>
                    <InputPanel onRunSimulation={handleRunSimulation} loading={loading} />
                </Sider>
                <Content style={{ padding: '24px', overflow: 'auto' }}>
                    <Spin spinning={loading} tip="Running simulation..." size="large">
                        {error && <Alert message="Error" description={error} type="error" showIcon closable onClose={() => setError(null)} style={{ marginBottom: 24 }} />}
                        {!simulationResults && !loading && !error && (
                            <Alert
                                message="Welcome to SimSXCu"
                                description="Select a simulation mode and enter your parameters on the left, then click 'Run Simulation' to see the results here."
                                type="info"
                                showIcon
                            />
                        )}
                        {simulationResults && <OutputPanel results={simulationResults} />}
                    </Spin>
                </Content>
            </Layout>
        </Layout>
    );
};

export default App;
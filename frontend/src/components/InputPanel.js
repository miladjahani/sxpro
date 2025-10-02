import React, { useState } from 'react';
import { Form, Input, Button, Select, Radio, Tooltip, Slider, Row, Col, Divider, InputNumber } from 'antd';
import { InfoCircleOutlined } from '@ant-design/icons';

const { Option } = Select;

const formItemLayout = {
    labelCol: { span: 24 },
    wrapperCol: { span: 24 },
};

// Tooltip text for each parameter
const tooltips = {
    PLS_flow: "Volume of pregnant leach solution fed to the plant.",
    PLS_Cu: "Concentration of copper in the PLS.",
    PLS_Ac: "Concentration of free acid in the PLS.",
    O_A_Ext: "Ratio of organic flow rate to aqueous flow rate in the extraction stages.",
    SP_Cu: "Concentration of copper in the electrolyte returning from the tankhouse.",
    SP_Ac: "Concentration of free acid in the electrolyte returning from the tankhouse.",
    AD_Cu: "Concentration of copper in the electrolyte advancing to the tankhouse.",
    Mef1s: "Efficiency of the first stripping mixer in achieving equilibrium.",
    SR: "The percentage of the organic's maximum loading capacity (AML) that is achieved.",
    Mef1e: "Efficiency of the first extraction mixer.",
    Mef2e: "Efficiency of the second extraction mixer.",
    ML_plant: "Actual measured copper concentration in the loaded organic from the plant.",
    raffinate_Cu_target: "The desired final copper concentration in the aqueous phase after extraction.",
    stripped_organic_Cu_target: "The desired final copper concentration in the organic phase after stripping."
};

const InputField = ({ name, label, unit, tooltip, children }) => (
    <Form.Item
        label={
            <span>
                {label} ({unit})&nbsp;
                <Tooltip title={tooltip}>
                    <InfoCircleOutlined />
                </Tooltip>
            </span>
        }
        name={name}
        rules={[{ required: true, message: `Please input the ${label}!` }]}
    >
        {children}
    </Form.Item>
);

// Custom controlled component to combine an InputNumber and a Slider.
// It receives `value` and `onChange` from the wrapping Form.Item.
const CombinedSliderInput = ({ value, onChange, min, max, step }) => {
    const handleValueChange = (newValue) => {
        // Ensure that a valid number is passed to the form, even if the input is cleared.
        const safeValue = newValue === null || newValue === undefined ? min : newValue;
        if (onChange) {
            onChange(safeValue);
        }
    };

    return (
        <Row align="middle">
            <Col span={12}>
                <InputNumber
                    min={min}
                    max={max}
                    step={step}
                    style={{ width: '95%', marginRight: '5%' }}
                    value={value}
                    onChange={handleValueChange}
                />
            </Col>
            <Col span={12}>
                <Slider
                    min={min}
                    max={max}
                    step={step}
                    onChange={handleValueChange}
                    value={typeof value === 'number' ? value : min}
                />
            </Col>
        </Row>
    );
};

const SliderInputField = ({ name, label, unit, tooltip, min, max, step }) => (
    <Form.Item
        label={
            <span>
                {label} ({unit})&nbsp;
                <Tooltip title={tooltip}>
                    <InfoCircleOutlined />
                </Tooltip>
            </span>
        }
        name={name}
        rules={[{ required: true, message: `Please input the ${label}!` }]}
    >
        <CombinedSliderInput min={min} max={max} step={step} />
    </Form.Item>
);

const InputPanel = ({ onRunSimulation, loading }) => {
    const [form] = Form.useForm();
    const [mode, setMode] = useState('designer');

    const onFinish = (values) => {
        // Convert all values from form (which can be strings) to numbers
        const numericValues = Object.entries(values).reduce((acc, [key, value]) => {
            acc[key] = (key === 'mode' || key === 'config') ? value : parseFloat(value);
            return acc;
        }, {});
        onRunSimulation(numericValues);
    };

    const handleModeChange = (e) => {
        setMode(e.target.value);
        form.resetFields(); // Reset fields when mode changes to avoid carrying over values
    };

    return (
        <Form
            {...formItemLayout}
            form={form}
            name="simulation_input"
            onFinish={onFinish}
            initialValues={{
                mode: 'designer',
                config: 'A',
                // Default values for faster testing
                PLS_flow: 400,
                PLS_Cu: 2.5,
                PLS_Ac: 1.6,
                O_A_Ext: 1,
                SP_Cu: 30,
                SP_Ac: 190,
                AD_Cu: 50,
                Mef1s: 98,
                SR: 92,
                Mef1e: 92,
                Mef2e: 95,
                ML_plant: 4.386,
                raffinate_Cu_target: 0.28,
                stripped_organic_Cu_target: 1.8,
            }}
            layout="vertical"
        >
            <Divider orientation="left">Configuration</Divider>
            <Form.Item name="config" label="Circuit Configuration">
                <Select>
                    <Option value="A">A: Series 2Ex1S</Option>
                    <Option value="B" disabled>B: Series 2Ex2S (Not Implemented)</Option>
                </Select>
            </Form.Item>

            <Form.Item name="mode" label="Simulation Mode">
                <Radio.Group onChange={handleModeChange}>
                    <Radio.Button value="designer">Designer</Radio.Button>
                    <Radio.Button value="plant">Plant Metallurgist</Radio.Button>
                </Radio.Group>
            </Form.Item>

            <Divider orientation="left">Process Parameters</Divider>

            <InputField name="PLS_flow" label="PLS Flow" unit="m³/h" tooltip={tooltips.PLS_flow}>
                <InputNumber style={{ width: '100%' }} />
            </InputField>
            <InputField name="PLS_Cu" label="PLS Copper" unit="g/L" tooltip={tooltips.PLS_Cu}>
                <InputNumber style={{ width: '100%' }} />
            </InputField>
            <InputField name="PLS_Ac" label="PLS Acid" unit="g/L" tooltip={tooltips.PLS_Ac}>
                <InputNumber style={{ width: '100%' }} />
            </InputField>
            <InputField name="O_A_Ext" label="Extraction O/A Ratio" unit="-" tooltip={tooltips.O_A_Ext}>
                <InputNumber style={{ width: '100%' }} />
            </InputField>

            <Divider orientation="left">Stripping & Electrolyte</Divider>

            <InputField name="SP_Cu" label="Spent Electrolyte Cu" unit="g/L" tooltip={tooltips.SP_Cu}>
                <InputNumber style={{ width: '100%' }} />
            </InputField>
            <InputField name="SP_Ac" label="Spent Electrolyte Acid" unit="g/L" tooltip={tooltips.SP_Ac}>
                <InputNumber style={{ width: '100%' }} />
            </InputField>
            <InputField name="AD_Cu" label="Advanced Electrolyte Cu" unit="g/L" tooltip={tooltips.AD_Cu}>
                <InputNumber style={{ width: '100%' }} />
            </InputField>
            <SliderInputField name="Mef1s" label="Stripping Mixer Eff." unit="%" tooltip={tooltips.Mef1s} min={70} max={100} step={1} />


            {mode === 'designer' ? (
                <>
                    <Divider orientation="left">Designer Mode Inputs</Divider>
                    <SliderInputField name="SR" label="Saturation Ratio" unit="%" tooltip={tooltips.SR} min={70} max={100} step={1} />
                    <SliderInputField name="Mef1e" label="Extraction Mixer Eff. 1" unit="%" tooltip={tooltips.Mef1e} min={70} max={100} step={1} />
                    <SliderInputField name="Mef2e" label="Extraction Mixer Eff. 2" unit="%" tooltip={tooltips.Mef2e} min={70} max={100} step={1} />
                </>
            ) : (
                <>
                    <Divider orientation="left">Plant Mode Inputs</Divider>
                    <InputField name="ML_plant" label="Plant Loaded Organic" unit="g/L" tooltip={tooltips.ML_plant}>
                         <InputNumber style={{ width: '100%' }} />
                    </InputField>
                    <InputField name="raffinate_Cu_target" label="Target Raffinate Cu" unit="g/L" tooltip={tooltips.raffinate_Cu_target}>
                         <InputNumber style={{ width: '100%' }} />
                    </InputField>
                    <InputField name="stripped_organic_Cu_target" label="Target Stripped Organic" unit="g/L" tooltip={tooltips.stripped_organic_Cu_target}>
                         <InputNumber style={{ width: '100%' }} />
                    </InputField>
                </>
            )}

            <Form.Item>
                <Button type="primary" htmlType="submit" loading={loading} style={{ width: '100%', marginTop: '24px' }}>
                    Run Simulation
                </Button>
            </Form.Item>
        </Form>
    );
};

export default InputPanel;
class FhsDemoDashboardStrategy extends HTMLElement {
  static noEditor = true;

  static getCreateSuggestions(_hass) {
    return {
      title: 'Flex Horseshoe Card Demo',
      icon: 'mdi:horseshoe',
    };
  }

  static async generate(_config, hass) {
    return hass.callWS({
      type: 'flex_horseshoe_card/demo_dashboard',
    });
  }
}


if (!customElements.get('ll-strategy-dashboard-fhs-demo')) {
  customElements.define(
    'll-strategy-dashboard-fhs-demo',
    FhsDemoDashboardStrategy,
  );
}


window.customStrategies = window.customStrategies || [];

if (!window.customStrategies.some(
  (strategy) => (
    strategy.type === 'fhs-demo'
    && strategy.strategyType === 'dashboard'
  ),
)) {
  window.customStrategies.push({
    type: 'fhs-demo',
    strategyType: 'dashboard',
    name: 'Flex Horseshoe Card Demo',
    description: 'Example dashboards using your own Home Assistant entities.',
  });
}

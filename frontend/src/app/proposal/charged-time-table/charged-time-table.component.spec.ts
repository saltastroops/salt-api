import { ChargedTimeTableComponent } from './charged-time-table.component';
import { render } from '@testing-library/angular';
import { ChargedTime, TimeAllocation } from '../../types';

describe('ChargedTimeTableComponent', () => {
  const charged_time: ChargedTime = {
    priority_0: 600,
    priority_1: 100,
    priority_2: 0,
    priority_3: 3000,
    priority_4: 2000,
  };
  const time_allocations: TimeAllocation[] = [
    {
      partner: { name: 'Aa', code: 'A', institute: 'Ai', department: 'Ad' },
      priority_0: 2000,
      priority_1: 60000,
      priority_2: 7000,
      priority_3: 600,
      priority_4: 3000,
      tac_comment:
        'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Doloremque laborum possimus  ' +
        'qui quisquam recusandae temporibus veritatis! Accusamus deserunt, illum.',
    },
    {
      partner: { name: 'Ba', code: 'B', institute: 'Bi', department: 'Bd' },
      priority_0: 2000,
      priority_1: 60000,
      priority_2: 7000,
      priority_3: 600,
      priority_4: 3000,
      tac_comment:
        'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Doloremque laborum possimus  ' +
        'qui quisquam recusandae temporibus veritatis! Accusamus deserunt, illum.',
    },
    {
      partner: { name: 'Ca', code: 'C', institute: 'Ci', department: 'Cd' },
      priority_0: 2000,
      priority_1: 60000,
      priority_2: 7000,
      priority_3: 600,
      priority_4: 3000,
      tac_comment:
        'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Doloremque laborum possimus  ' +
        'qui quisquam recusandae temporibus veritatis! Accusamus deserunt, illum.',
    },
    {
      partner: { name: 'Da', code: 'D', institute: 'Di', department: 'Dd' },
      priority_0: 2000,
      priority_1: 60000,
      priority_2: 7000,
      priority_3: 600,
      priority_4: 3000,
      tac_comment:
        'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Doloremque laborum possimus  ' +
        'qui quisquam recusandae temporibus veritatis! Accusamus deserunt, illum.',
    },
  ];

  it('should create', async () => {
    const component = await render(ChargedTimeTableComponent, {
      componentProperties: {
        charged_time,
        time_allocation: time_allocations[0],
      },
    });
    expect(component).toBeTruthy();
  });

  it('should display the correct absolute completion', async () => {
    const component = await render(ChargedTimeTableComponent, {
      componentProperties: {
        charged_time,
        time_allocation: time_allocations[0],
      },
    });
    const completion = component.getByTestId('absolute-completion');
    expect(completion.innerText).toContain('3700/69600');
  });

  it('should display the correct relative completion', async () => {
    const component = await render(ChargedTimeTableComponent, {
      componentProperties: {
        charged_time,
        time_allocation: time_allocations[0],
      },
    });
    const completion = component.getByTestId('relative-completion');
    expect(completion.innerText).toContain('5.3%');
  });
});

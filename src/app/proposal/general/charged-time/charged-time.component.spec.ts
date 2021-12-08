import { ChargedTimeComponent } from './charged-time.component';
import { render } from '@testing-library/angular';
import { ChargedTime, TimeAllocation } from '../../../types/proposal';

describe('ChargedTimeTableComponent', () => {
  const charged_time: ChargedTime = {
    priority0: 600,
    priority1: 100,
    priority2: 0,
    priority3: 3000,
    priority4: 2000,
  };
  const time_allocations: TimeAllocation[] = [
    {
      partnerName: 'South Africa',
      partnerCode: 'RSA',
      priority0: 2000,
      priority1: 60000,
      priority2: 7000,
      priority3: 600,
      priority4: 3000,
      tacComment:
        'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Doloremque laborum possimus  ' +
        'qui quisquam recusandae temporibus veritatis! Accusamus deserunt, illum.',
    },
    {
      partnerName: 'South Africa',
      partnerCode: 'RSA',
      priority0: 2000,
      priority1: 60000,
      priority2: 7000,
      priority3: 600,
      priority4: 3000,
      tacComment:
        'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Doloremque laborum possimus  ' +
        'qui quisquam recusandae temporibus veritatis! Accusamus deserunt, illum.',
    },
    {
      partnerName: 'South Africa',
      partnerCode: 'RSA',
      priority0: 2000,
      priority1: 60000,
      priority2: 7000,
      priority3: 600,
      priority4: 3000,
      tacComment:
        'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Doloremque laborum possimus  ' +
        'qui quisquam recusandae temporibus veritatis! Accusamus deserunt, illum.',
    },
    {
      partnerName: 'South Africa',
      partnerCode: 'RSA',
      priority0: 2000,
      priority1: 60000,
      priority2: 7000,
      priority3: 600,
      priority4: 3000,
      tacComment:
        'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Doloremque laborum possimus  ' +
        'qui quisquam recusandae temporibus veritatis! Accusamus deserunt, illum.',
    },
  ];

  it('should create', async () => {
    const component = await render(ChargedTimeComponent, {
      componentProperties: {
        chargedTime: charged_time,
        timeAllocation: time_allocations[0],
      },
    });
    expect(component).toBeTruthy();
  });

  it('should display the correct absolute completion', async () => {
    const component = await render(ChargedTimeComponent, {
      componentProperties: {
        chargedTime: charged_time,
        timeAllocation: time_allocations[0],
      },
    });
    const completion = component.getByTestId('absolute-completion');
    expect(completion.innerText).toContain('3700/69600');
  });

  it('should display the correct relative completion', async () => {
    const component = await render(ChargedTimeComponent, {
      componentProperties: {
        chargedTime: charged_time,
        timeAllocation: time_allocations[0],
      },
    });
    const completion = component.getByTestId('relative-completion');
    expect(completion.innerText).toContain('5.3%');
  });
});

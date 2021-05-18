import { Proposal } from '../types';

export const proposal: Proposal = {
  investigators: [
    {
      name: 'John Doe Leader',
      partner: {
        name: 'South Africa',
        code: 'RSA',
        institute: 'SAAO',
        department: '',
      },
      is_pc: true,
      is_pi: true,
      accept: true,
    },
    {
      name: 'John Doe Second',
      partner: {
        name: 'South Africa',
        code: 'RSA',
        institute: 'University of Cape Town',
        department: 'Department of Astronomy',
      },
      is_pc: false,
      is_pi: false,
      accept: false,
    },
    {
      name: 'Mary Jane',
      partner: {
        name: 'Other',
        code: 'OTH',
        institute: 'University of Wakanda',
        department: '',
      },
      is_pc: false,
      is_pi: false,
      accept: false,
    },
    {
      name: 'Thomas DaFirst',
      partner: {
        name: 'UK SALT Consortium',
        code: 'UK',
        institute: 'Open University',
        department: 'Physics and Astronomy',
      },
      is_pc: false,
      is_pi: false,
      accept: false,
    },
    {
      name: 'John Doe Member',
      partner: {
        name: 'South Africa',
        code: 'RSA',
        institute: 'University of Cape Town',
        department: 'Department of Astronomy',
      },
      is_pc: false,
      is_pi: false,
      accept: false,
    },
  ],
};

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
  general_info: {
    id: 23654,
    code: '2020-1-MLT-005',
    title: 'Lorem ipsum dolor sit amet.',
    abstract:
      'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ab debitis nesciunt perspiciatis praesentium, ' +
      'provident reprehenderit rerum. Ab alias architecto asperiores assumenda atque autem cumque dolorum eius error et ' +
      'eveniet excepturi, expedita illo illum incidunt ipsam minima modi nulla pariatur quasi quidem, quisquam ' +
      'soluta sunt? Eos eum necessitatibus nostrum soluta veniam.',
    current_submission: new Date(2020, 3, 31),
    first_submission: new Date(2019, 11, 30),
    submission_number: 12,
    phase: 2,
    current_semester: { year: 2021, semester: 2 },
    semesters: [
      { year: 2020, semester: 1 },
      { year: 2020, semester: 2 },
      { year: 2021, semester: 1 },
      { year: 2021, semester: 2 },
    ],
    status: {
      status: 'active',
      message: 'The proposal has been added to the queue.',
    },
  },
};

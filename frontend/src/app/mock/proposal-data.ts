import { Proposal } from '../types/proposal';

export const proposal: any = {
  investigators: [
    {
      id: 1,
      name: 'Drake Blane',
      partner: {
        name: 'South Africa',
        code: 'RSA',
        institute: 'SAAO',
        department: '',
      },
      is_pc: true,
      is_pi: true,
    },
    {
      id: 2,
      name: 'John Doe Second',
      partner: {
        name: 'South Africa',
        code: 'RSA',
        institute: 'University of Cape Town',
        department: 'Department of Astronomy',
      },
      is_pc: false,
      is_pi: false,
    },
    {
      id: 3,
      name: 'Mary Jane',
      partner: {
        name: 'Other',
        code: 'OTH',
        institute: 'University of Wakanda',
        department: '',
      },
      is_pc: false,
      is_pi: false,
    },
    {
      id: 4,
      name: 'Thomas DaFirst',
      partner: {
        name: 'UK SALT Consortium',
        code: 'UK',
        institute: 'Open University',
        department: 'Physics and Astronomy',
      },
      is_pc: false,
      is_pi: false,
    },
    {
      id: 5,
      name: 'John Doe Member',
      partner: {
        name: 'South Africa',
        code: 'RSA',
        institute: 'University of Cape Town',
        department: 'Department of Astronomy',
      },
      is_pc: false,
      is_pi: false,
    },
    {
      id: 6,
      name: 'Jane Foster',
      partner: {
        name: 'South Africa',
        code: 'RSA',
        institute: 'SAAO',
        department: '',
      },
      is_pc: false,
      is_pi: false,
    },
  ],
  generalInfo: {
    id: 23654,
    code: '2020-1-MLT-005',
    title: 'Lorem ipsum dolor sit amet.',
    abstract:
      'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ab debitis nesciunt perspiciatis praesentium, ' +
      'provident reprehenderit rerum. Ab alias architecto asperiores assumenda atque autem cumque dolorum eius error et ' +
      'eveniet excepturi, expedita illo illum incidunt ipsam minima modi nulla pariatur quasi quidem, quisquam ' +
      'soluta sunt? Eos eum necessitatibus nostrum soluta veniam.',
    currentSubmission: new Date(2020, 3, 31),
    firstSubmission: new Date(2019, 11, 30),
    submissionNumber: 12,
    phase: 2,
    currentSemester: { year: 2021, semester: 2 },
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
    type: 'Science - Long Term',
    targetOfOpportunity: false,
    totalRequestedTime: 9999,
    proprietaryPeriod: 36,
    responsibleSaltAstronomer: {
      given_name: 'John',
      family_name: 'Doe',
      email: 'johndoe.@host.com',
    },
    summaryForSaltAstronomer: `
----------------------------------
Lorem ipsum dolor.
----------------------------------

Lorem ipsum dolor sit amet, consectetur adipisicing elit. Consequatur, facere.
Lorem ipsum dolor sit amet, consectetur adipisicing elit.

----------------------------------
Lorem ipsum dolor sit amet.
----------------------------------

Lorem ipsum dolor sit amet, consectetur adipisicing elit. Atque error eveniet illo iure sapiente sunt vero. Ad
architecto, beatae blanditiis debitis deleniti doloremque incidunt itaque natus nisi, nostrum quidem sint!
Lorem ipsum dolor sit amet, consectetur adipisicing elit. Consequuntur doloremque error inventore nemo quae rerum!
Lorem ipsum dolor sit amet, consectetur adipisicing elit. Blanditiis error et, nulla optio soluta voluptas.

- Lorem ipsum dolor sit amet, consectetur adipisicing elit. Maxime, totam!
- Lorem ipsum dolor sit amet, consectetur adipisicing elit.
- Lorem ipsum dolor sit amet, consectetur.
- Lorem ipsum dolor sit amet, consectetur adipisicing elit. Accusantium laboriosam libero nemo nesciunt temporibus. Aliquid!
- Lorem ipsum dolor sit amet, consectetur adipisicing elit. Eligendi, ullam!
- Lorem ipsum dolor sit amet, consectetur adipisicing elit. Impedit libero maxime similique unde voluptatem.
- Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ipsum?
- Lorem ipsum dolor sit amet, consectetur adipisicing elit. Esse eum expedita neque provident quas recusandae sapiente, veritatis voluptates! Animi, obcaecati.
- Lorem ipsum dolor sit amet, consectetur adipisicing elit. Atque cupiditate fugit, molestiae quasi quos reprehenderit vel voluptatum! Autem debitis dolorem ducimus esse ex exercitationem expedita ipsa iusto modi optio pariatur perferendis, placeat quasi quia quibusdam temporibus tenetur unde ut voluptatem.
- Lorem ipsum dolor sit amet, consectetur adipisicing elit. At debitis est eum libero repellendus ullam!

----------------------------------
Lorem ipsum dolor.
----------------------------------

Lorem ipsum dolor sit amet, consectetur adipisicing elit. Laboriosam, omnis.
Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ab architecto, beatae cumque, dicta dolores dolorum eius et expedita explicabo hic id omnis porro quas repellendus ullam veniam, veritatis vero. Culpa.
`,
    summaryForNightLog:
      'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Deleniti ducimus est, et incidunt labore nam nisi officia quos reiciendis repudiandae sit sunt tempora voluptas, voluptatem?\n',
  },
  blocks: [
    {
      id: 1234,
      name: 'block name 1',
      obs_time: 2391,
      priority: 2,
      requested_block_visits: 2,
      done_visits: 1,
      observable_tonight: false,
      remaining_nights: 50,
      maximum_seeing: 2,
      transparency: 'Thin cloud',
      maximum_lunar_phase: 14.6,
      instruments: [{ name: 'RSS', config_mode: 'Spectroscopy' }],
    },
    {
      id: 2234,
      name: 'block name 2',
      obs_time: 2391,
      priority: 3,
      requested_block_visits: 2,
      done_visits: 0,
      observable_tonight: false,
      remaining_nights: 50,
      maximum_seeing: 2.5,
      transparency: 'Thin cloud',

      maximum_lunar_phase: 14.6,
      instruments: [{ name: 'RSS', config_mode: 'Spectroscopy' }],
    },
    {
      id: 3234,
      name: 'block name 3',
      obs_time: 2391,
      priority: 1,
      requested_block_visits: 2,
      done_visits: 1,
      observable_tonight: true,
      remaining_nights: 50,
      maximum_seeing: 2.5,
      transparency: 'Clear',

      maximum_lunar_phase: 14.6,
      instruments: [{ name: 'RSS', config_mode: 'Spectroscopy' }],
    },
    {
      id: 4234,
      name: 'block name 4',
      obs_time: 2391,
      priority: 2,
      requested_block_visits: 2,
      done_visits: 1,
      observable_tonight: false,
      remaining_nights: 50,
      maximum_seeing: 2,
      transparency: 'Any',

      maximum_lunar_phase: 14.6,
      instruments: [{ name: 'RSS', config_mode: 'Spectroscopy' }],
    },
    {
      id: 5234,
      name: 'block name 5',
      obs_time: 2391,
      priority: 1,
      requested_block_visits: 2,
      done_visits: 1,
      observable_tonight: false,
      remaining_nights: 50,
      maximum_seeing: 2,
      transparency: 'Thin cloud',

      maximum_lunar_phase: 14.6,
      instruments: [{ name: 'RSS', config_mode: 'Spectroscopy' }],
    },
    {
      id: 6234,
      name: 'block name 6',
      obs_time: 6391,
      priority: 0,
      requested_block_visits: 6,
      done_visits: 3,
      observable_tonight: true,
      remaining_nights: 50,
      maximum_seeing: 3,
      transparency: 'Any',

      maximum_lunar_phase: 14.6,
      instruments: [{ name: 'RSS', config_mode: 'Spectroscopy' }],
    },
    {
      id: 7234,
      name: 'block name 7',
      obs_time: 2391,
      priority: 2,
      requested_block_visits: 2,
      done_visits: 1,
      observable_tonight: false,
      remaining_nights: 56,
      maximum_seeing: 1,
      transparency: 'Thick cloud',

      maximum_lunar_phase: 14.6,
      instruments: [
        { name: 'RSS', config_mode: 'Spectroscopy' },
        { name: 'SCAM', config_mode: 'Imaging' },
      ],
    },
    {
      id: 8234,
      name: 'block name 8',
      obs_time: 3365,
      priority: 2,
      requested_block_visits: 2,
      done_visits: 1,
      observable_tonight: true,
      remaining_nights: 50,
      maximum_seeing: 2,
      transparency: 'Clear',

      maximum_lunar_phase: 14.6,
      instruments: [{ name: 'RSS', config_mode: 'Spectroscopy' }],
    },
    {
      id: 8234,
      name: 'block name 8',
      obs_time: 4391,
      priority: 0,
      requested_block_visits: 8,
      done_visits: 2,
      observable_tonight: true,
      remaining_nights: 15,
      maximum_seeing: 2.5,
      transparency: 'Clear',

      maximum_lunar_phase: 14.6,
      instruments: [{ name: 'RSS', config_mode: 'Spectroscopy' }],
    },
    {
      id: 10234,
      name: 'block name 10',
      obs_time: 5041,
      priority: 2,
      requested_block_visits: 2,
      done_visits: 1,
      observable_tonight: false,
      remaining_nights: 16,
      maximum_seeing: 2,
      transparency: 'Thick cloud',

      maximum_lunar_phase: 14.6,
      instruments: [
        { name: 'RSS', config_mode: 'Spectroscopy' },
        { name: 'HRS', config_mode: 'LR' },
        { name: 'SCAM', config_mode: 'Imaging' },
      ],
    },
    {
      id: 11234,
      name: 'block name 11',
      obs_time: 62194,
      priority: 4,
      requested_block_visits: 10,
      done_visits: 9,
      observable_tonight: true,
      remaining_nights: 10,
      maximum_seeing: 1,
      transparency: 'Thick cloud',

      maximum_lunar_phase: 14.6,
      instruments: [{ name: 'RSS', config_mode: 'Spectroscopy' }],
    },
  ],
  executedObservations: [
    {
      observation_id: 6677,
      block_identifier: {
        id: 12341,
        name: 'Block name 1',
      },
      observation_time: 100,
      priority: 1,
      maximum_lunar_phase: 14.5,
      targets: ['Target name 1', 'target name 2'],
      observation_date: new Date(2019, 11, 30),
      accepted: true,
      rejection_reason: null,
    },
    {
      observation_id: 7814,
      block_identifier: {
        id: 12342,
        name: 'Block name 2',
      },
      observation_time: 100,
      priority: 1,
      maximum_lunar_phase: 14.5,
      targets: ['Target name 3'],
      observation_date: new Date(2019, 11, 30),
      accepted: false,
      rejection_reason:
        'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Atque dolores laborum veritatis.',
    },
    {
      observation_id: 8134,
      block_identifier: {
        id: 12343,
        name: 'Block name 3',
      },
      observation_time: 100,
      priority: 1,
      maximum_lunar_phase: 14.5,
      targets: ['Target name 5'],
      observation_date: new Date(2019, 11, 30),
      accepted: true,
      rejection_reason: null,
    },
  ],
  timeAllocations: [
    {
      partner: {
        name: 'South Africa',
        code: 'RSA',
        institute: '',
        department: '',
      },
      priority0: 2700,
      priority1: 66700,
      priority2: 7100,
      priority3: 6700,
      priority4: 112700,
      tacComment:
        'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Doloremque laborum possimus  ' +
        'qui quisquam recusandae temporibus veritatis! Accusamus deserunt, illum.',
    },
    {
      partner: {
        name: 'University of Wisconsin-Madison',
        code: 'UW',
        institute: '',
        department: '',
      },
      priority0: 2700,
      priority1: 0,
      priority2: 0,
      priority3: 0,
      priority4: 112700,
      tacComment:
        'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Doloremque laborum possimus  ' +
        'qui quisquam recusandae temporibus veritatis! Accusamus deserunt, illum.',
    },
    {
      partner: {
        name: 'UK SALT Consortium',
        code: 'UK',
        institute: '',
        department: '',
      },
      priority0: 0,
      priority1: 66700,
      priority2: 700,
      priority3: 0,
      priority4: 22700,
      tacComment: null,
    },
    {
      partner: { name: 'Poland', code: 'POL', institute: '', department: '' },
      priority0: 2700,
      priority1: 0,
      priority2: 700,
      priority3: 3362,
      priority4: 12700,
      tacComment: null,
    },
  ],
  chargedTime: {
    priority0: 659,
    priority1: 0,
    priority2: 0,
    priority3: 34999,
    priority4: 27966,
  },
  comments: [
    {
      author: 'Robbert Smith',
      comment: `Lorem ipsum dolor sit amet, consectetur adipisicing elit. Accusamus debitis doloremque harum in libero neque quidem saepe sunt? Adipisci aliquid asperiores eaque enim, est harum id iure minus obcaecati officia similique, suscipit tempore voluptates voluptatum?

Lorem ipsum dolor sit amet, consectetur adipisicing elit. Alias consectetur est ex harum illum inventore libero quibusdam quisquam sapiente soluta?
`,
      madeAt: new Date(2020, 0, 15, 9, 4, 6, 6),
    },
    {
      author: 'John Doe',
      comment: `Lorem ipsum dolor sit amet, consectetur adipisicing elit. Accusamus debitis doloremque harum in libero neque quidem saepe sunt? Adipisci aliquid asperiores eaque enim, est harum id iure minus obcaecati officia similique, suscipit tempore voluptates voluptatum?

Lorem ipsum dolor sit amet, consectetur adipisicing elit. Alias consectetur est ex harum illum inventore libero quibusdam quisquam sapiente soluta?

Lorem ipsum dolor sit amet, consectetur adipisicing elit. Amet consequatur deleniti facilis quaerat reprehenderit. Accusantium asperiores beatae debitis delectus distinctio eaque expedita itaque laborum maiores maxime mollitia perspiciatis quibusdam, voluptas. Asperiores atque expedita perspiciatis quisquam. Cupiditate ex, impedit incidunt laborum laudantium omnis porro, quas quia quo quos repellat sapiente sunt?
  `,
      madeAt: new Date(2020, 1, 6, 10, 34, 36, 6),
    },
    {
      author: 'Robbert Smith',
      comment: `Lorem ipsum dolor sit amet, consectetur adipisicing elit. Accusamus debitis doloremque harum in libero neque quidem saepe sunt? Adipisci aliquid asperiores eaque enim, est harum id iure minus obcaecati officia similique, suscipit tempore voluptates voluptatum?

Lorem ipsum dolor sit amet, consectetur adipisicing elit. Alias consectetur est ex harum illum inventore libero quibusdam quisquam sapiente soluta?
`,
      madeAt: new Date(2020, 2, 15, 9, 4, 6, 6),
    },
    {
      author: 'Jacob May',
      comment: `Lorem ipsum dolor sit amet, consectetur adipisicing elit. Accusamus debitis doloremque harum in libero neque quidem saepe sunt? Adipisci aliquid asperiores eaque enim, est harum id iure minus obcaecati officia similique, suscipit tempore voluptates voluptatum?`,
      madeAt: new Date(2020, 4, 23, 13, 34, 6, 6),
    },
  ],
  progress: null,
  proposalAcceptance: [
    {
      investigatorId: 1,
      accepted: true,
    },
    {
      investigatorId: 2,
      accepted: true,
    },
    {
      investigatorId: 3,
      accepted: false,
    },
    {
      investigatorId: 4,
      accepted: null,
    },
    {
      investigatorId: 5,
      accepted: false,
    },
    {
      investigatorId: 6,
      accepted: true,
    },
  ],
};
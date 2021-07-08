import { addHours, addMinutes } from 'date-fns';
import { Block } from '../types';

export const blockGeneralDetails: Block = {
  id: 33,
  name: 'Block name 33',
  observingConditions: {
    transparency: 'Thin clouds',
    minimumLunarPhase: 14.5,
    maximumLunarPhase: 14.5,
    minimumLunarDistance: 14.5,
    minimumSeeing: 0.1,
    maximumSeeing: 2,
    observationTime: 2000,
  },
  wait: 2,
  visits: 3,
  attempted: 3,
  done: 3,
  shutterOpenTime: 1400,
  overheads: 900,
  observationTime: 3000,
  priority: 1,
  comment: `
Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ab animi aperiam atque autem commodi consequuntur culpa deserunt, doloribus ea earum et ex expedita facere, fuga ipsam ipsum iste, iure magnam magni maxime minus modi nesciunt numquam odit praesentium quas quasi quis quisquam quo quod ratione reiciendis sunt veritatis.

Assumenda corporis, debitis earum harum mollitia officia officiis quia repudiandae sed voluptate.
Dolores eligendi itaque magnam minus, officiis provident quibusdam recusandae? Ab aspernatur assumenda beatae, consequatur dicta doloribus ducimus earum excepturi fuga ipsa iste iure magnam minus nam nemo nobis odio odit officiis perferendis perspiciatis reiciendis rem tempore ut, vero vitae voluptas.
    `,
  observingWindows: [
    {
      start: new Date(2020, 7, 11, 3, 0, 0),
      end: new Date(2020, 7, 11, 4, 0, 0),
      type: 'Strict',
    },
    {
      start: new Date(),
      end: addMinutes(new Date(), 20),
      type: 'Strict',
    },
    {
      start: addHours(new Date(), 60),
      end: addHours(new Date(), 61),
      type: 'Strict',
    },
    {
      start: addHours(new Date(), 22),
      end: addHours(new Date(), 23),
      type: 'Strict',
    },
    {
      start: addHours(new Date(), 25),
      end: addHours(new Date(), 26),
      type: 'Strict',
    },
    {
      start: new Date(2020, 7, 13, 3, 0, 0),
      end: new Date(2020, 7, 13, 4, 0, 0),
      type: 'Strict',
    },
    {
      start: new Date(2020, 7, 14, 3, 0, 0),
      end: new Date(2020, 7, 14, 4, 0, 0),
      type: 'Strict',
    },
    {
      start: new Date(2020, 7, 11, 3, 0, 0),
      end: new Date(2020, 7, 11, 4, 0, 0),
      type: 'Strict',
    },
    {
      start: new Date(2020, 7, 12, 3, 0, 0),
      end: new Date(2020, 7, 12, 4, 0, 0),
      type: 'Strict',
    },
    {
      start: new Date(2020, 7, 13, 3, 0, 0),
      end: new Date(2020, 7, 13, 4, 0, 0),
      type: 'Strict',
    },
    {
      start: new Date(2020, 7, 14, 3, 0, 0),
      end: new Date(2020, 7, 14, 4, 0, 0),
      type: 'Strict',
    },
    {
      start: new Date(2020, 7, 11, 3, 0, 0),
      end: new Date(2020, 7, 11, 4, 0, 0),
      type: 'Strict',
    },
    {
      start: new Date(2020, 7, 12, 3, 0, 0),
      end: new Date(2020, 7, 12, 4, 0, 0),
      type: 'Strict',
    },
    {
      start: new Date(2020, 7, 13, 3, 0, 0),
      end: new Date(2020, 7, 13, 4, 0, 0),
      type: 'Strict',
    },
    {
      start: new Date(2020, 7, 14, 3, 0, 0),
      end: new Date(2020, 7, 14, 4, 0, 0),
      type: 'Strict',
    },
    {
      start: new Date(2020, 7, 11, 3, 0, 0),
      end: new Date(2020, 7, 11, 4, 0, 0),
      type: 'Strict',
    },
    {
      start: new Date(2020, 7, 12, 3, 0, 0),
      end: new Date(2020, 7, 12, 4, 0, 0),
      type: 'Strict',
    },
    {
      start: new Date(2020, 7, 13, 3, 0, 0),
      end: new Date(2020, 7, 13, 4, 0, 0),
      type: 'Strict',
    },
    {
      start: new Date(2020, 7, 14, 3, 0, 0),
      end: new Date(2020, 7, 14, 4, 0, 0),
      type: 'Strict',
    },
    {
      start: new Date(2020, 7, 11, 3, 0, 0),
      end: new Date(2020, 7, 11, 4, 0, 0),
      type: 'Strict',
    },
    {
      start: new Date(2020, 7, 12, 3, 0, 0),
      end: new Date(2020, 7, 12, 4, 0, 0),
      type: 'Strict',
    },
    {
      start: new Date(2020, 7, 13, 3, 0, 0),
      end: new Date(2020, 7, 13, 4, 0, 0),
      type: 'Strict',
    },
    {
      start: new Date(2020, 7, 14, 3, 0, 0),
      end: new Date(2020, 7, 14, 4, 0, 0),
      type: 'Strict',
    },
    {
      start: new Date(2020, 7, 11, 3, 0, 0),
      end: new Date(2020, 7, 11, 4, 0, 0),
      type: 'Strict',
    },
    {
      start: new Date(2020, 7, 12, 3, 0, 0),
      end: new Date(2020, 7, 12, 4, 0, 0),
      type: 'Strict',
    },
    {
      start: new Date(2020, 7, 13, 3, 0, 0),
      end: new Date(2020, 7, 13, 4, 0, 0),
      type: 'Strict',
    },
    {
      start: new Date(2020, 7, 14, 3, 0, 0),
      end: new Date(2020, 7, 14, 4, 0, 0),
      type: 'Strict',
    },
    {
      start: new Date(2020, 7, 11, 3, 0, 0),
      end: new Date(2020, 7, 11, 4, 0, 0),
      type: 'Strict',
    },
    {
      start: new Date(2020, 7, 12, 3, 0, 0),
      end: new Date(2020, 7, 12, 4, 0, 0),
      type: 'Strict',
    },
    {
      start: new Date(2020, 7, 13, 3, 0, 0),
      end: new Date(2020, 7, 13, 4, 0, 0),
      type: 'Strict',
    },
    {
      start: new Date(2020, 7, 14, 3, 0, 0),
      end: new Date(2020, 7, 14, 4, 0, 0),
      type: 'Strict',
    },
    {
      start: new Date(2020, 7, 11, 3, 0, 0),
      end: new Date(2020, 7, 11, 4, 0, 0),
      type: 'Strict',
    },
    {
      start: new Date(2020, 7, 12, 3, 0, 0),
      end: new Date(2020, 7, 12, 4, 0, 0),
      type: 'Strict',
    },
    {
      start: new Date(2020, 7, 13, 3, 0, 0),
      end: new Date(2020, 7, 13, 4, 0, 0),
      type: 'Strict',
    },
    {
      start: new Date(2020, 7, 14, 3, 0, 0),
      end: new Date(2020, 7, 14, 4, 0, 0),
      type: 'Strict',
    },
    {
      start: new Date(2020, 7, 11, 3, 0, 0),
      end: new Date(2020, 7, 11, 4, 0, 0),
      type: 'Strict',
    },
    {
      start: new Date(2020, 7, 12, 3, 0, 0),
      end: new Date(2020, 7, 12, 4, 0, 0),
      type: 'Strict',
    },
    {
      start: new Date(2020, 7, 13, 3, 0, 0),
      end: new Date(2020, 7, 13, 4, 0, 0),
      type: 'Strict',
    },
    {
      start: new Date(2020, 7, 14, 3, 0, 0),
      end: new Date(2020, 7, 14, 4, 0, 0),
      type: 'Strict',
    },
  ],
  observationProbabilities: {
    moon: 0.15,
    competition: 0.15,
    observability: 0.15,
    seeing: 0.15,
    averageRanking: 30.123,
    total: 0.3,
  },
  lastModified: new Date(2020, 4, 16),
};

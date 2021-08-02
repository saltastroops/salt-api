import {Hrs} from "../../types";

export const hrs: Hrs =
  {
    name: "[Hrs]",
    hrsConfig: {
      mode: 'MEDIUM RESOLUTION',
      exposureType: 'Science',
      nodAndShuffle: {
        nodCount: undefined,
        nodInterval: undefined,
      },
      iodineCellPosition: 'OUT',
      targetLocation: 'STAR',
      fibreSeparation: 60.0,
      useThArWithIodineCell: false,
    },
    hrsProcedure: {
      cycles: 1,
      blueExposurePattern: [480],
      redExposurePattern: [480],
    },
    hrsBlueDetector: {
      readoutSpeed: 'Slow',
      preBinCols: 1,
      preBinRows: 1,
      iterations: 1,
      postShuffle: 0,
      preShuffle: 0,
      numberOfAmplifiers: 1,
    },
    hrsRedDetector: {
      readoutSpeed: 'Slow',
      preBinCols: 1,
      preBinRows: 1,
      iterations: 1,
      postShuffle: 0,
      preShuffle: 0,
      numberOfAmplifiers: 1,
    },
    shutterOpenTime: 486.00,
    overhead: 0,
    charged: 485.00
  }


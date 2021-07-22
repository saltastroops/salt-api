import {Salticam} from "../../types";

export const salticam: Salticam =  {
  inCalibration: false,
  salticamDetector: {
    preBinCols: 2,
    preBinRows: 2,
    exposureType: "Science",
    readoutSpeed: "Fast",
    detMode: "Normal",
    iterations: 1,
    gain: "Bright"
  },
  minimumSN: 0,
  cycles: 1,
  name: "[Salticam]",
  salticamProcedure: [
    {
    name: "U-S1",
    filter: "Johnson U",
    exposureTime: 1,
    },
    {
      name: "B-S1",
      filter: "Johnson B",
      exposureTime: 1,
    },
    {
      name: "V-S1",
      filter: "Johnson V",
      exposureTime: 1,
    },
  ],
  shutterOpenTime: 14,
  overhead: 15,
  charged: 13,
  }

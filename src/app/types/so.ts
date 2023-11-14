import { FinderChart, GuideStar } from "./observation";
import { SalticamExposure } from "./salticam";

export interface Acquisition {
  targetName: string;
  finderCharts: FinderChart[];
  guideStar: GuideStar | null;
  maximumSeeing: number;
  exposures: SalticamExposure[];
}

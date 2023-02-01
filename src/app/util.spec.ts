import { parseISO } from "date-fns";

import { FinderChart, FinderChartFile } from "./types/observation";
import { currentJulianDay, finderChartURL } from "./util";

describe("util", () => {
  beforeEach(() => {
    jasmine.clock().install();
  });

  afterEach(() => {
    jasmine.clock().uninstall();
  });

  it("should return the correct finder chart URL", () => {
    const files: FinderChartFile[] = [
      { size: "original", url: "/o.png" },
      { size: "thumbnail", url: "/t.pdf" },
      { size: "thumbnail", url: "/t.jpg" },
      { size: "original", url: "/o.pdf" },
    ];
    const finderChart = { files } as FinderChart;
    const baseURL = "https://example.com";

    expect(
      finderChartURL(
        finderChart,
        ["original", "thumbnail"],
        ["pdf", "jpg"],
        baseURL,
      ),
    ).toEqual("https://example.com/o.pdf");
    expect(
      finderChartURL(finderChart, ["original", "thumbnail"], ["jpg"], baseURL),
    ).toEqual("https://example.com/t.jpg");
    expect(
      finderChartURL(finderChart, ["original"], ["jpg"], baseURL),
    ).toBeNull();
    expect(
      finderChartURL(
        finderChart,
        ["original", "thumbnail"],
        ["jpg", "png", "pdf"],
        baseURL,
      ),
    ).toEqual("https://example.com/o.png");
    expect(
      finderChartURL(
        finderChart,
        ["thumbnail", "thumbnail"],
        ["jpg", "png", "pdf"],
        baseURL,
      ),
    ).toEqual("https://example.com/t.jpg");
  });

  it("should calculate the correct current Julian day", () => {
    const checkJulianDay = (
      now: string,
      expectedStart: string,
      expectedEnd: string,
    ) => {
      jasmine.clock().mockDate(parseISO(now));
      const jd = currentJulianDay();
      expect(jd.start).toEqual(parseISO(expectedStart));
      expect(jd.end).toEqual(parseISO(expectedEnd));
      console.log(parseISO("2022-09-09T12:00:00+02"));
    };

    checkJulianDay(
      "2022-05-06T12:00:00Z",
      "2022-05-06T12:00:00Z",
      "2022-05-07T12:00:00Z",
    );
    checkJulianDay(
      "2023-01-01T11:59:59Z",
      "2022-12-31T12:00:00Z",
      "2023-01-01T12:00:00Z",
    );
    checkJulianDay(
      "2023-06-30T23:12:19Z",
      "2023-06-30T12:00:00Z",
      "2023-07-01T12:00:00Z",
    );
  });
});

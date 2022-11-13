import { FinderChart, FinderChartFile } from "./types/observation";
import { finderChartURL } from "./util";

describe("util", () => {
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
});

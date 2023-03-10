import { Investigator } from "./types/proposal";
import { User } from "./types/user";
import {
  convertRightAscensionHMSToDegrees,
  degreesToDms,
  degreesToHms,
  isPrincipalContact,
  isPrincipalInvestigator,
} from "./utils";

const investigators = [
  {
    givenName: "Principal",
    familyName: "Investigator",
    email: "pi@email.yes",
    isPi: true,
    isPc: false,
  } as Investigator,
  {
    givenName: "Principal",
    familyName: "Contact",
    email: "pc@email.yes",
    isPi: false,
    isPc: true,
  } as Investigator,
  {
    givenName: "Just",
    familyName: "Investigator",
    email: "investigator@email.yes",
    isPi: false,
    isPc: false,
  } as Investigator,
];

describe("degreesToDms", () => {
  it("should return 55.23456 degrees in degrees:minutes:seconds", () => {
    expect(degreesToDms(55.23456)).toEqual("+55:14:04.42");
  });

  it("should return 12.9999 degrees in degrees:minutes:seconds", () => {
    expect(degreesToDms(12.9999999)).toEqual("+13:00:00.00");
  });

  it("should return -23.1234567 degrees in degrees:minutes:seconds (seconds formatted to 3 decimal places)", () => {
    expect(degreesToDms(-23.1234567, 3)).toEqual("-23:07:24.444");
  });

  it("should return 0 degrees in degrees:minutes:seconds", () => {
    expect(degreesToDms(0)).toEqual("+00:00:00.00");
  });

  it("should return 8.5 degrees in degrees:minutes:seconds", () => {
    expect(degreesToDms(8.5)).toEqual("+08:30:00.00");
  });
});

describe("Unit test for angle (degrees) to hours:minutes:seconds conversion functions", () => {
  it("should return 55.23456 degrees in hours:minutes:seconds", () => {
    expect(degreesToHms(55.23456)).toEqual("03:40:56.29");
  });

  it("should return 59.99999999 degrees in hours:minutes:seconds", () => {
    expect(degreesToHms(59.99999999)).toEqual("04:00:00.00");
  });

  it("should return 200.23456 degrees in hours:minutes:seconds (seconds formatted to 3 decimal places)", () => {
    expect(degreesToHms(200.23456, 3)).toEqual("13:20:56.294");
  });

  it("should return 0 degrees in hours:minutes:seconds", () => {
    expect(degreesToHms(0)).toEqual("00:00:00.00");
  });

  it("should return 22.5 degrees in hours:minutes:seconds", () => {
    expect(degreesToHms(22.5)).toEqual("01:30:00.00");
  });

  it("should raise an error for a negative degrees value", () => {
    expect(() => degreesToHms(-55.23456)).toThrowError(/negative/);
  });
});

describe("Unit test for hours:minutes:seconds to angle (degrees) conversion functions ", () => {
  it("It should work", () => {
    expect(convertRightAscensionHMSToDegrees("0:10:10")).toBeCloseTo(
      2.541667,
      5,
    );
    expect(convertRightAscensionHMSToDegrees("10:10:10")).toBeCloseTo(
      152.54166666666666,
      5,
    );
    expect(convertRightAscensionHMSToDegrees("10:0:10")).toBeCloseTo(
      150.04166666666669,
      5,
    );
    expect(convertRightAscensionHMSToDegrees("10:10:00")).toBeCloseTo(152.5, 5);
  });
  it("should return 0 degrees for 0:00:00", () => {
    expect(convertRightAscensionHMSToDegrees("0:00:00")).toBeCloseTo(0, 5);
  });

  it("should return 180 degrees for 12:00:00", () => {
    expect(convertRightAscensionHMSToDegrees("12:00:00")).toBeCloseTo(180, 5);
  });

  it("should return 22.5 degrees for 01:30:00.00", () => {
    expect(convertRightAscensionHMSToDegrees("01:30:00.00")).toBeCloseTo(
      22.5,
      5,
    );
  });

  it("should return 60 for 04:00:00.00", () => {
    expect(convertRightAscensionHMSToDegrees("04:00:00.00")).toBeCloseTo(60, 5);
  });

  it("should default seconds to 0, if seconds are not provided", () => {
    expect(convertRightAscensionHMSToDegrees("04:00")).toBeCloseTo(60, 5);
  });

  it("should default seconds and minutes to 0, if seconds and minutes are not provided", () => {
    expect(convertRightAscensionHMSToDegrees("04")).toBeCloseTo(60, 5);
  });

  it("should raise an error for a negative hours", () => {
    expect(() =>
      convertRightAscensionHMSToDegrees("-04:00:00.00"),
    ).toThrowError(/less than 0/);
  });
  it("should raise an error for an invalid format", () => {
    [
      "::",
      ":05:05:05",
      ":05:05:05:",
      "05:05:05:",
      ":05:",
      ":05",
      "05'",
      "05;",
      "05,",
      "05.",
      '05"',
      "05 ",
      "12.5.0.9",
    ].forEach((ra) => {
      expect(() => convertRightAscensionHMSToDegrees(ra)).toThrowError(
        /Right ascension is invalid/,
      );
    });
  });

  it("should raise an error for hours greater or equal to 24", () => {
    expect(() => convertRightAscensionHMSToDegrees("25:00:15")).toThrowError(
      /between 0 and 23/,
    );
    expect(() => convertRightAscensionHMSToDegrees("24:00:00")).toThrowError(
      /between 0 and 23/,
    );
  });

  it("should raise an error for minutes greater than or equal to 60", () => {
    expect(() => convertRightAscensionHMSToDegrees("12:60:30")).toThrowError(
      /not be greater than or equal to 60/,
    );
  });

  it("should raise an error for seconds greater or equal to 60", () => {
    expect(() => convertRightAscensionHMSToDegrees("12:30:60")).toThrowError(
      /not be greater than or equal to 60/,
    );
  });
  it("should raise an error for characters", () => {
    expect(() => convertRightAscensionHMSToDegrees("aa:30:60")).toThrowError(
      /Right ascension is invalid/,
    );
    expect(() => convertRightAscensionHMSToDegrees("aa:bb:60")).toThrowError(
      /Right ascension is invalid/,
    );
    expect(() => convertRightAscensionHMSToDegrees("12:30:cc")).toThrowError(
      /Right ascension is invalid/,
    );
    expect(() => convertRightAscensionHMSToDegrees("12:bb:cc")).toThrowError(
      /Right ascension is invalid/,
    );
    expect(() => convertRightAscensionHMSToDegrees("aa:bb:60")).toThrowError(
      /Right ascension is invalid/,
    );
    expect(() => convertRightAscensionHMSToDegrees("aa:bb:cc")).toThrowError(
      /Right ascension is invalid/,
    );
  });
});

describe("Unit test to check if user is a principal investigator", () => {
  it("It should work", () => {
    [
      {
        user: {
          givenName: "Principal",
          familyName: "Investigator",
          email: "pi@email.yes",
        } as User,
        investigators,
        expected: true,
      },
      {
        user: {
          givenName: "Principal",
          familyName: "Investigator",
          email: "pc@email.yes",
        } as User,
        investigators,
        expected: false,
      },
      {
        user: {
          givenName: "Just",
          familyName: "Investigator",
          email: "investigator@email.yes",
        } as User,
        investigators,
        expected: false,
      },
    ].forEach((e) => {
      expect(() => isPrincipalInvestigator(e.user, e.investigators)).toEqual(
        e.expected,
      );
    });
  });
});

describe("Unit test to check if user is a principal contact", () => {
  it("It should work", () => {
    [
      {
        user: {
          givenName: "Principal",
          familyName: "Investigator",
          email: "pi@email.yes",
        } as User,
        investigators,
        expected: false,
      },
      {
        user: {
          givenName: "Principal",
          familyName: "Investigator",
          email: "pc@email.yes",
        } as User,
        investigators,
        expected: true,
      },
      {
        user: {
          givenName: "Just",
          familyName: "Investigator",
          email: "investigator@email.yes",
        } as User,
        investigators,
        expected: false,
      },
    ].forEach((e) => {
      expect(() => isPrincipalContact(e.user, e.investigators)).toEqual(
        e.expected,
      );
    });
  });
});

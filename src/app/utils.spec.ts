import { degreesToDms, degreesToHms } from './utils';

describe('degreesToDms', () => {
  it('should return 55.23456 degrees in degrees:minutes:seconds', () => {
    expect(degreesToDms(55.23456)).toEqual('+55:14:04.42');
  });

  it('should return 12.9999 degrees in degrees:minutes:seconds', () => {
    expect(degreesToDms(12.9999999)).toEqual('+13:00:00.00');
  });

  it('should return -23.1234567 degrees in degrees:minutes:seconds (seconds formatted to 3 decimal places)', () => {
    expect(degreesToDms(-23.1234567, 3)).toEqual('-23:07:24.444');
  });

  it('should return 0 degrees in degrees:minutes:seconds', () => {
    expect(degreesToDms(0)).toEqual('+00:00:00.00');
  });

  it('should return 8.5 degrees in degrees:minutes:seconds', () => {
    expect(degreesToDms(8.5)).toEqual('+08:30:00.00');
  });
});

describe('Unit test for angle (degrees) to hours:minutes:seconds conversion functions', () => {
  it('should return 55.23456 degrees in hours:minutes:seconds', () => {
    expect(degreesToHms(55.23456)).toEqual('03:40:56.29');
  });

  it('should return 59.99999999 degrees in hours:minutes:seconds', () => {
    expect(degreesToHms(59.99999999)).toEqual('04:00:00.00');
  });

  it('should return 200.23456 degrees in hours:minutes:seconds (seconds formatted to 3 decimal places)', () => {
    expect(degreesToHms(200.23456, 3)).toEqual('13:20:56.294');
  });

  it('should return 0 degrees in hours:minutes:seconds', () => {
    expect(degreesToHms(0)).toEqual('00:00:00.00');
  });

  it('should return 22.5 degrees in hours:minutes:seconds', () => {
    expect(degreesToHms(22.5)).toEqual('01:30:00.00');
  });

  it('should raise an error for a negative degrees value', () => {
    expect(() => degreesToHms(-55.23456)).toThrowError(/negative/);
  });
});

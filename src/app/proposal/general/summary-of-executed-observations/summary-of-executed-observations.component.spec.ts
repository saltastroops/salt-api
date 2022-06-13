import { TestBed } from "@angular/core/testing";

import { fireEvent, render } from "@testing-library/angular";
import { DateFnsModule } from "ngx-date-fns";
import { of } from "rxjs";

import { AuthenticationService } from "../../../service/authentication.service";
import { BlockVisit } from "../../../types/common";
import { User } from "../../../types/user";
import { SummaryOfExecutedObservationsComponent } from "./summary-of-executed-observations.component";

describe("SummaryOfExecutedObservationsComponent", () => {
  const blockVisits: BlockVisit[] = [
    {
      id: 567,
      blockId: 6677,
      blockName: "Block name 1",
      observationTime: 100,
      priority: 1,
      maximumLunarPhase: 14.5,
      targets: ["Target name 1", "target name 2"],
      night: "2019-11-30",
      status: "Accepted",
      rejectionReason: null,
    },
    {
      id: 12342,
      blockId: 7814,
      blockName: "Block name 2",
      observationTime: 100,
      priority: 1,
      maximumLunarPhase: 14.5,
      targets: ["Target name 3"],
      night: "2019-11-30",
      status: "Rejected",
      rejectionReason:
        "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Atque dolores laborum veritatis.",
    },
  ];

  const expectedUser: User = {
    id: 1,
    username: "Jdoe",
    givenName: "John",
    familyName: "Doe",
    email: "johndoe@exmaple.com",
    alternativeEmails: [],
    roles: [],
    affiliations: [
      {
        institutionId: 1,
        name: "Institution A",
        partnerCode: "RSA",
        partnerName: "Partner A",
        department: "",
      },
    ],
  };

  beforeEach(async () => {
    const getUserSpy = jasmine.createSpyObj("AuthenticationService", {
      getUser: of(expectedUser),
    });

    await TestBed.configureTestingModule({
      declarations: [SummaryOfExecutedObservationsComponent],
      imports: [DateFnsModule.forRoot()],
      providers: [{ provide: AuthenticationService, useValue: getUserSpy }],
    }).compileComponents();
  });

  it("should create", async () => {
    const component = await render(SummaryOfExecutedObservationsComponent, {
      componentProperties: {
        blockVisits,
      },
    });
    expect(component).toBeTruthy();
  });

  it("should toggle an observation when the observation's checkbox is clicked", async () => {
    const component = await render(SummaryOfExecutedObservationsComponent, {
      componentProperties: {
        blockVisits,
      },
    });
    const observationCheckbox1 = component.getAllByTestId(
      "download-observation-checkbox",
    )[0] as HTMLInputElement;
    const observationCheckbox2 = component.getAllByTestId(
      "download-observation-checkbox",
    )[1] as HTMLInputElement;
    expect(observationCheckbox1.checked).toBeFalse();
    expect(observationCheckbox2.checked).toBeFalse();

    observationCheckbox2.click();
    expect(observationCheckbox1.checked).toBeFalse();
    expect(observationCheckbox2.checked).toBeTrue();

    observationCheckbox2.click();
    expect(observationCheckbox1.checked).toBeFalse();
    expect(observationCheckbox1.checked).toBeFalse();
  });

  it('should select/deselect all if the "Select/Deselect all" checkbox is clicked', async () => {
    const component = await render(SummaryOfExecutedObservationsComponent, {
      componentProperties: {
        blockVisits,
      },
    });
    const selectAllSelector = component.getByTestId(
      "select-all-observations-checkbox",
    );
    const checkboxes = component.getAllByTestId(
      "download-observation-checkbox",
    );

    // Click Select/Deselect all
    fireEvent.click(selectAllSelector);
    expect((selectAllSelector as HTMLInputElement).checked).toBeTruthy();

    // All observations have been selected.
    expect(checkboxes.every((e) => (e as HTMLInputElement).checked)).toBeTrue();

    // Click Select/Deselect all
    fireEvent.click(selectAllSelector);
    expect((selectAllSelector as HTMLInputElement).checked).toBeFalsy();

    // All observations have been deselected
    expect(
      checkboxes.every((e) => (e as HTMLInputElement).checked),
    ).toBeFalse();
  });

  it('should select/deselect the "Select/Deselect all" (only) if all observations are selected', async () => {
    const component = await render(SummaryOfExecutedObservationsComponent, {
      componentProperties: {
        blockVisits,
      },
    });
    const selectAllCheckbox = component.getByTestId(
      "select-all-observations-checkbox",
    ) as HTMLInputElement;
    const observationCheckboxes = component.getAllByTestId(
      "download-observation-checkbox",
    );

    // Select the first observation
    observationCheckboxes[0].click();

    // The Select/Deselect all checkbox is still unchecked
    expect(selectAllCheckbox.checked);

    // After selecting all the remaining observations, the Select/Deselect all checkbox
    // is checked
    observationCheckboxes.slice(1).forEach((c) => {
      c.click();
    });
    expect(selectAllCheckbox.checked).toBeFalse();

    // After unselecting the first observation, the Select/Deselect all checkbox is
    // unchecked again
    fireEvent.click(observationCheckboxes[0]);
    expect(selectAllCheckbox.checked).toBeFalse();

    // Unselecting all the other observations doesn't change the Select/Deselect all
    // checkbox
    observationCheckboxes.slice(1).forEach((c) => {
      c.click();
    });
    expect(selectAllCheckbox.checked).toBeFalse();
  });
});

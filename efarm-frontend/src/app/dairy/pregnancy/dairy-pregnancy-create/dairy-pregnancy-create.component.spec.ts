import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DairyPregnancyCreateComponent } from './dairy-pregnancy-create.component';

describe('DairyPregnancyCreateComponent', () => {
  let component: DairyPregnancyCreateComponent;
  let fixture: ComponentFixture<DairyPregnancyCreateComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DairyPregnancyCreateComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DairyPregnancyCreateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

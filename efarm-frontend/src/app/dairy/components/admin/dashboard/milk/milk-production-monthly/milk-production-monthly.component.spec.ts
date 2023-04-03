import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MilkProductionMonthlyComponent } from './milk-production-monthly.component';

describe('MilkProductionMonthlyComponent', () => {
  let component: MilkProductionMonthlyComponent;
  let fixture: ComponentFixture<MilkProductionMonthlyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MilkProductionMonthlyComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MilkProductionMonthlyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

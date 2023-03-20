import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TotalAliveMaleCowsComponent } from './total-alive-male-cows.component';

describe('TotalAliveMaleCowsComponent', () => {
  let component: TotalAliveMaleCowsComponent;
  let fixture: ComponentFixture<TotalAliveMaleCowsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TotalAliveMaleCowsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TotalAliveMaleCowsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

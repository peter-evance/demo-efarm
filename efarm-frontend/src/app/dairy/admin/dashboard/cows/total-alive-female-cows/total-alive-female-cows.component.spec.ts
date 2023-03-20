import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TotalAliveFemaleCowsComponent } from './total-alive-female-cows.component';

describe('TotalAliveFemaleCowsComponent', () => {
  let component: TotalAliveFemaleCowsComponent;
  let fixture: ComponentFixture<TotalAliveFemaleCowsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TotalAliveFemaleCowsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TotalAliveFemaleCowsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

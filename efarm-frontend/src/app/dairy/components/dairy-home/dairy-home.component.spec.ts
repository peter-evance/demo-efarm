import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DairyHomeComponent } from './dairy-home.component';

describe('DairyHomeComponent', () => {
  let component: DairyHomeComponent;
  let fixture: ComponentFixture<DairyHomeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DairyHomeComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DairyHomeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

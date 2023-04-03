import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DairyContactUsComponent } from './dairy-contact-us.component';

describe('DairyContactUsComponent', () => {
  let component: DairyContactUsComponent;
  let fixture: ComponentFixture<DairyContactUsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DairyContactUsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DairyContactUsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
